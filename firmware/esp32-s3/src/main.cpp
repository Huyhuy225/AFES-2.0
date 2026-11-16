#include <Arduino.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <esp_mac.h>
#include <esp_random.h>
#include <time.h>

#include "config.h"
#if __has_include("secrets.h")
#include "secrets.h"
#else
#include "secrets.example.h"
#endif

namespace {

WiFiClient g_wifi_client;
PubSubClient g_mqtt_client(g_wifi_client);

char g_mac_str[18] = "00:00:00:00:00:00";
char g_topic_telemetry[128];
char g_topic_status[128];
char g_topic_cmd_req[128];
char g_topic_cmd_res[128];

unsigned long g_last_telemetry_ms = 0;
unsigned long g_last_safety_ms = 0;
unsigned long g_last_mqtt_attempt_ms = 0;
unsigned long g_manual_override_until_ms = 0;
constexpr unsigned long MQTT_RECONNECT_INTERVAL_MS = 5000UL;

bool g_buzzer_active = false;
bool g_alarm_led_active = false;
bool g_pump_relay_active = false;
const char *g_override_mode = "AUTO";

void readHardwareMac() {
    uint8_t mac[6] = {0};
    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    snprintf(
        g_mac_str,
        sizeof(g_mac_str),
        "%02X:%02X:%02X:%02X:%02X:%02X",
        mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]
    );
}

void generateUuidV4(char *out, size_t len) {
    uint8_t bytes[16];
    for (int i = 0; i < 16; i += 4) {
        uint32_t r = esp_random();
        bytes[i] = (r >> 24) & 0xFF;
        bytes[i + 1] = (r >> 16) & 0xFF;
        bytes[i + 2] = (r >> 8) & 0xFF;
        bytes[i + 3] = r & 0xFF;
    }
    bytes[6] = (bytes[6] & 0x0F) | 0x40;  // Version 4
    bytes[8] = (bytes[8] & 0x3F) | 0x80;  // RFC 4122 variant
    snprintf(
        out,
        len,
        "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x",
        bytes[0], bytes[1], bytes[2], bytes[3],
        bytes[4], bytes[5], bytes[6], bytes[7],
        bytes[8], bytes[9], bytes[10], bytes[11],
        bytes[12], bytes[13], bytes[14], bytes[15]
    );
}

void applyActuators() {
    digitalWrite(PIN_BUZZER, g_buzzer_active ? HIGH : LOW);
    digitalWrite(PIN_ALARM_LED, g_alarm_led_active ? HIGH : LOW);
    digitalWrite(PIN_PUMP_RELAY, g_pump_relay_active ? HIGH : LOW);
}

void runLocalSafetyLoop() {
    // TODO(Stage-B-Hardware): Replace with calibrated MQ-2, flame, and temp/humidity drivers.
    const int smoke_adc = analogRead(PIN_MQ2_SMOKE_ADC);
    const int flame_adc = analogRead(PIN_FLAME_ADC);
    const bool flame_detected = (digitalRead(PIN_FLAME_DO) == LOW);
    const float smoke_ppm = (smoke_adc / 4095.0f) * 1000.0f;

    // Local safety behavior MUST NEVER depend on Wi-Fi/MQTT/WAN availability.
    if (strcmp(g_override_mode, "MANUAL_OVERRIDE") == 0 &&
        g_manual_override_until_ms != 0 &&
        static_cast<long>(millis() - g_manual_override_until_ms) >= 0) {
        g_override_mode = "AUTO";
        g_manual_override_until_ms = 0;
    }

    if (strcmp(g_override_mode, "AUTO") == 0) {
        const bool critical = flame_detected || (smoke_ppm >= SMOKE_CRITICAL_PPM);
        const bool warning = !critical && (smoke_ppm >= SMOKE_WARNING_PPM);
        g_alarm_led_active = critical || warning;
        g_buzzer_active = critical;
        g_pump_relay_active = critical;
        applyActuators();
    }
    (void)flame_adc;
}

void handleCommand(char *topic, byte *payload, unsigned int length) {
    (void)topic;
    JsonDocument doc;
    if (deserializeJson(doc, payload, length) != DeserializationError::Ok) {
        return;
    }

    const char *action = doc["action"] | "";
    const char *request_id = doc["request_id"] | "";
    bool ok = true;

    if (strcmp(action, "PUMP_ON") == 0) {
        g_override_mode = "MANUAL_OVERRIDE";
        g_pump_relay_active = true;
        const unsigned long duration_ms = doc["parameters"]["duration_ms"] | 0UL;
        g_manual_override_until_ms = (duration_ms > 0) ? (millis() + duration_ms) : 0;
    } else if (strcmp(action, "PUMP_OFF") == 0) {
        g_pump_relay_active = false;
        g_override_mode = "AUTO";
        g_manual_override_until_ms = 0;
    } else if (strcmp(action, "EMERGENCY_RELEASE") == 0 || strcmp(action, "RESET_ALERTS") == 0) {
        g_override_mode = "AUTO";
        g_manual_override_until_ms = 0;
        g_buzzer_active = false;
        g_alarm_led_active = false;
        g_pump_relay_active = false;
    } else if (strcmp(action, "REBOOT_DEVICE") == 0) {
        ESP.restart();
    } else {
        ok = false;
    }
    applyActuators();

    JsonDocument res;
    res["schema_version"] = AFES_SCHEMA_VERSION;
    res["request_id"] = request_id;
    res["device_id"] = AFES_DEVICE_ID;
    res["action"] = action;
    res["status"] = ok ? "SUCCESS" : "REJECTED";
    res["status_code"] = ok ? 200 : 400;

    char out[256];
    serializeJson(res, out, sizeof(out));
    g_mqtt_client.publish(g_topic_cmd_res, out, false);
}

void ensureMqttConnected() {
    if (WiFi.status() != WL_CONNECTED || g_mqtt_client.connected()) {
        return;
    }
    const unsigned long now = millis();
    if (g_last_mqtt_attempt_ms != 0 && (now - g_last_mqtt_attempt_ms) < MQTT_RECONNECT_INTERVAL_MS) {
        return;
    }
    g_last_mqtt_attempt_ms = now;
    if (g_mqtt_client.connect(
            AFES_DEVICE_ID,
            MQTT_USERNAME,
            MQTT_PASSWORD,
            g_topic_status,
            1,
            true,
            "OFFLINE")) {
        g_mqtt_client.publish(g_topic_status, "ONLINE", true);
        g_mqtt_client.subscribe(g_topic_cmd_req, 1);
        Serial.println("[MQTT] Connected and subscribed to command/req");
    }
}

void publishTelemetry() {
    if (!g_mqtt_client.connected()) {
        return;
    }

    const int smoke_adc = constrain(analogRead(PIN_MQ2_SMOKE_ADC), 0, 4095);
    const int flame_adc = constrain(analogRead(PIN_FLAME_ADC), 0, 4095);
    const bool flame_detected = (digitalRead(PIN_FLAME_DO) == LOW);
    const float smoke_ppm = (smoke_adc / 4095.0f) * 1000.0f;

    char msg_id[37];
    generateUuidV4(msg_id, sizeof(msg_id));

    struct timeval tv;
    gettimeofday(&tv, nullptr);
    const int64_t epoch_ms = static_cast<int64_t>(tv.tv_sec) * 1000LL + (tv.tv_usec / 1000LL);
    struct tm tm_utc;
    gmtime_r(&tv.tv_sec, &tm_utc);
    char utc_buf[25];
    snprintf(
        utc_buf,
        sizeof(utc_buf),
        "%04d-%02d-%02dT%02d:%02d:%02d.%03ldZ",
        tm_utc.tm_year + 1900,
        tm_utc.tm_mon + 1,
        tm_utc.tm_mday,
        tm_utc.tm_hour,
        tm_utc.tm_min,
        tm_utc.tm_sec,
        tv.tv_usec / 1000L
    );

    JsonDocument doc;
    doc["schema_version"] = AFES_SCHEMA_VERSION;
    doc["message_id"] = msg_id;
    doc["correlation_id"] = nullptr;

    JsonObject device = doc["device"].to<JsonObject>();
    device["device_id"] = AFES_DEVICE_ID;
    device["device_type"] = AFES_DEVICE_TYPE;
    device["firmware_version"] = AFES_FIRMWARE_VERSION;
    device["hardware_version"] = AFES_HARDWARE_VERSION;
    device["mac_address"] = g_mac_str;

    JsonObject zone = doc["zone"].to<JsonObject>();
    zone["zone_id"] = AFES_ZONE_ID;
    zone["room_code"] = AFES_ROOM_CODE;
    zone["building_id"] = AFES_BUILDING_ID;
    zone["floor_level"] = AFES_FLOOR_LEVEL;

    JsonObject gateway = doc["gateway"].to<JsonObject>();
    gateway["gateway_id"] = AFES_GATEWAY_ID;
    gateway["protocol"] = AFES_GATEWAY_PROTOCOL;
    gateway["mesh_role"] = AFES_MESH_ROLE;

    JsonObject timestamps = doc["timestamps"].to<JsonObject>();
    timestamps["timestamp_utc"] = utc_buf;
    timestamps["timestamp_epoch_ms"] = epoch_ms;
    timestamps["device_uptime_s"] = millis() / 1000UL;

    JsonObject status = doc["status"].to<JsonObject>();
    status["system_state"] = g_pump_relay_active ? "CRITICAL" : "NORMAL";
    status["sensor_health"] = "HEALTHY";
    status["battery_pct"] = nullptr;
    status["rssi_dbm"] = WiFi.RSSI();

    JsonObject readings = doc["readings"].to<JsonObject>();
    // TODO(Stage-B-Hardware): Replace placeholder temp/humidity with real sensor driver.
    readings["temperature"] = 25.0;
    readings["humidity"] = 60.0;
    readings["smoke_ppm"] = smoke_ppm;
    readings["smoke_raw_adc"] = smoke_adc;
    readings["flame_detected"] = flame_detected;
    readings["flame_raw_adc"] = flame_adc;

    JsonObject actuators = doc["actuators"].to<JsonObject>();
    actuators["buzzer_active"] = g_buzzer_active;
    actuators["alarm_led_active"] = g_alarm_led_active;
    actuators["water_pump_relay_active"] = g_pump_relay_active;
    actuators["override_mode"] = g_override_mode;

    // Stage B physical hardware marker (MUST be false on ESP32-S3 firmware)
    JsonObject simulation = doc["simulation"].to<JsonObject>();
    simulation["is_simulated"] = false;
    simulation["scenario_id"] = nullptr;
    simulation["synthetic_noise_added"] = false;

    char payload[1024];
    serializeJson(doc, payload, sizeof(payload));
    g_mqtt_client.publish(g_topic_telemetry, payload, false);
}

}  // namespace

void setup() {
    Serial.begin(115200);
    pinMode(PIN_FLAME_DO, INPUT);
    pinMode(PIN_BUZZER, OUTPUT);
    pinMode(PIN_ALARM_LED, OUTPUT);
    pinMode(PIN_PUMP_RELAY, OUTPUT);
    applyActuators();

    analogReadResolution(12);
    readHardwareMac();

    snprintf(g_topic_telemetry, sizeof(g_topic_telemetry), "afes/v2/%s/devices/%s/telemetry", AFES_TENANT_ID, AFES_DEVICE_ID);
    snprintf(g_topic_status, sizeof(g_topic_status), "afes/v2/%s/devices/%s/status", AFES_TENANT_ID, AFES_DEVICE_ID);
    snprintf(g_topic_cmd_req, sizeof(g_topic_cmd_req), "afes/v2/%s/devices/%s/command/req", AFES_TENANT_ID, AFES_DEVICE_ID);
    snprintf(g_topic_cmd_res, sizeof(g_topic_cmd_res), "afes/v2/%s/devices/%s/command/res", AFES_TENANT_ID, AFES_DEVICE_ID);

    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    configTime(0, 0, "pool.ntp.org", "time.nist.gov");

    g_mqtt_client.setServer(MQTT_BROKER_HOST, MQTT_BROKER_PORT);
    g_mqtt_client.setBufferSize(1024);
    g_mqtt_client.setCallback(handleCommand);

    Serial.printf("[BOOT] AFES 2.0 Stage B Foundation | MAC=%s\n", g_mac_str);
}

void loop() {
    const unsigned long now = millis();
    if (now - g_last_safety_ms >= SAFETY_LOOP_INTERVAL_MS) {
        g_last_safety_ms = now;
        runLocalSafetyLoop();
    }

    ensureMqttConnected();
    g_mqtt_client.loop();

    if (now - g_last_telemetry_ms >= TELEMETRY_INTERVAL_MS) {
        g_last_telemetry_ms = now;
        publishTelemetry();
    }
}
