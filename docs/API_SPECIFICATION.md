# AFES 2.0 Backend REST and WebSocket API Specification

> **Specification Version**: 2.0.0
> **Status**: Approved Architecture Baseline
> **Base URL**: `/api/v2`
> **WebSocket Stream URL**: `/ws/v2/stream`
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)

---

## 1. Architectural Principles and Security Boundary

### 1.1. Core Security Invariant: Browser Isolation from CoreIOT
> **MANDATORY SECURITY INVARIANT**:
> Web browsers and mobile clients **MUST NEVER** receive, store, or transmit CoreIOT administrative tokens, device access tokens, or platform credentials.

The Spring Boot Application Server serves as the sole trusted intermediary, enforcing:
1. **User Identity & Role-Based Access Control (RBAC)**: All user actions are authenticated via standard JWT Bearer tokens.
2. **CoreIOT Mediation**: The backend securely manages tenant-level CoreIOT credentials, translating frontend user intent into CoreIOT REST/RPC calls or MQTT commands. Detailed CoreIOT platform onboarding, attribute mappings, and credentials handling are deferred to Issue #3.
3. **Audit Logging**: Every manual actuator trigger, alarm override, and emergency shutdown is recorded in an immutable audit log.

```
+------------------+         JWT Bearer          +-----------------------+
|  React Frontend  | -------------------------> |  Spring Boot Backend  |
|  (Web Browser)   |                            |  (Security Boundary)  |
+------------------+                            +-----------------------+
         |                                                  |
         X  DIRECT ACCESS STRICTLY FORBIDDEN                | CoreIOT Internal API
         |                                                  v
+--------------------+                          +-----------------------+
|   CoreIOT Server   | <----------------------- |   Local IoT Gateway   |
| (Platform-Neutral) |       Sync Protocol      |   (PC / RPi Edge)     |
+--------------------+                          +-----------------------+
```

---

## 2. Authentication, Roles, and Authorization

All requests to `/api/v2/*` (except public health checks and login) require an `Authorization` header:
```http
Authorization: Bearer <jwt_access_token>
```

### 2.1. Role Hierarchy and Permissions

| Role | Description | Permitted Capabilities |
|---|---|---|
| `ROLE_ADMIN` | System administrator | Full administrative control: zone/device CRUD, manual pump/siren overrides, emergency shutdowns, simulation injection, user management. |
| `ROLE_OPERATOR` | Safety officer / operator | Acknowledge active alarms, trigger periodic self-tests, view live telemetry and sensor health. Cannot delete devices or modify zones. |
| `ROLE_VIEWER` | Resident / viewer | Read-only access to dashboard views, floor plan summaries, and historical charts. No control or acknowledgment permissions. |
| `ROLE_GATEWAY` | Local IoT Gateway machine account | Ingest local aggregated telemetry, synchronize offline buffers, submit edge AI inference results, report gateway heartbeat. |

---

## 3. Standard Response and Error Envelope

All API responses adhere to a predictable JSON wrapper.

### 3.1. Success Response Structure

```json
{
  "success": true,
  "timestamp": 1794457200000,
  "data": { ... }
}
```

### 3.2. Error Response Structure

```json
{
  "success": false,
  "timestamp": 1794457200000,
  "error": {
    "code": "ERR_VALIDATION_FAILED",
    "message": "Invalid request parameter: duration_ms exceeds maximum permitted threshold (60000 ms)",
    "trace_id": "trc-8f192b-09",
    "details": [
      {
        "field": "duration_ms",
        "rejected_value": 120000,
        "constraint": "Must be between 1000 and 60000"
      }
    ]
  }
}
```

### 3.3. Standard Error Codes

| HTTP Status | Error Code | Description |
|---|---|---|
| `400 Bad Request` | `ERR_BAD_REQUEST` | Malformed JSON or invalid syntax. |
| `400 Bad Request` | `ERR_VALIDATION_FAILED` | Field-level parameter constraint failure. |
| `401 Unauthorized` | `ERR_UNAUTHORIZED` | Missing or expired JWT authentication token. |
| `403 Forbidden` | `ERR_FORBIDDEN` | Caller lacks the role required for this endpoint. |
| `404 Not Found` | `ERR_NOT_FOUND` | Referenced device, zone, or alarm does not exist. |
| `409 Conflict` | `ERR_DEVICE_BUSY` | Conflicting manual command currently in execution. |
| `422 Unprocessable`| `ERR_SIMULATION_LOCKED` | Simulated command attempted in Stage B physical production mode. |
| `502 Bad Gateway` | `ERR_GATEWAY_OFFLINE` | Target Local Gateway or node unreachable. |
| `503 Unavailable` | `ERR_COREIOT_UNAVAILABLE` | CoreIOT platform synchronization temporarily unavailable. |

---

## 4. REST Endpoints Specification

### 4.1. Authentication Services

#### `POST /api/v2/auth/login`
Authenticates user credentials and issues JWT tokens.
* **Access**: Public
* **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "<PASSWORD_PLACEHOLDER>"
  }
  ```
* **Response `200 OK`**:
  ```json
  {
    "success": true,
    "timestamp": 1794457200000,
    "data": {
      "access_token": "eyJhbGciOi...",
      "refresh_token": "def502...",
      "token_type": "Bearer",
      "expires_in_seconds": 3600,
      "user": {
        "id": "usr-01",
        "username": "admin",
        "role": "ROLE_ADMIN",
        "assigned_zone": null
      }
    }
  }
  ```

#### `GET /api/v2/auth/me`
Retrieves currently authenticated user profile.
* **Access**: `ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`
* **Response `200 OK`**: Returns user metadata and permissions.

---

### 4.2. Spatial Zones and Rooms

#### `GET /api/v2/zones`
Lists all monitored zones in the facility.
* **Access**: `ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`

#### `GET /api/v2/zones/summary`
Returns high-level real-time status summary across all zones for the primary dashboard map.
* **Access**: `ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`
* **Response `200 OK`**:
  ```json
  {
    "success": true,
    "timestamp": 1794457200000,
    "data": [
      {
        "zone_id": "ZONE-101",
        "room_code": "ROOM-101",
        "name": "Server Equipment Room",
        "floor": 1,
        "system_state": "NORMAL",
        "active_alarm_count": 0,
        "latest_readings": {
          "temperature": 24.5,
          "humidity": 55.2,
          "smoke_ppm": 45.0,
          "flame_detected": false
        },
        "actuator_state": {
          "buzzer_active": false,
          "pump_active": false
        },
        "node_count": 2,
        "last_updated_epoch_ms": 1794457198000
      }
    ]
  }
  ```

#### `POST /api/v2/zones`
Creates a new monitoring zone.
* **Access**: `ROLE_ADMIN`

---

### 4.3. Device and Sensing Node Management

#### `GET /api/v2/devices`
Lists registered devices with operational metrics.
* **Query Parameters**:
  * `zone_id` (string, optional)
  * `status` (string: `ONLINE`, `OFFLINE`, `FAULT`, optional)
  * `is_simulated` (boolean, optional)
* **Access**: `ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`

#### `GET /api/v2/devices/{deviceId}/health`
Returns granular self-diagnostic health, signal strength, uptime, and battery state.
* **Access**: `ROLE_OPERATOR`, `ROLE_ADMIN`
* **Response `200 OK`**:
  ```json
  {
    "success": true,
    "timestamp": 1794457200000,
    "data": {
      "device_id": "ESP32S3-YOLO-01",
      "status": "ONLINE",
      "sensor_health": "HEALTHY",
      "uptime_seconds": 128450,
      "rssi_dbm": -62,
      "heap_free_bytes": 194560,
      "tinyml_inference_latency_ms": 24,
      "is_simulated": false,
      "last_seen_epoch_ms": 1794457199500
    }
  }
  ```

---

### 4.4. Telemetry and Historical Analytics

#### `GET /api/v2/telemetry/latest`
Retrieves the most recent telemetry packet for a specific zone or device.
* **Query Parameters**:
  * `device_id` (string, optional)
  * `zone_id` (string, optional)
* **Access**: `ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`

#### `GET /api/v2/telemetry/history`
Queries historical time-series telemetry with pagination and filtering.
* **Query Parameters**:
  * `device_id` (string, required)
  * `from_epoch_ms` (integer, required)
  * `to_epoch_ms` (integer, required)
  * `page` (integer, default `0`)
  * `size` (integer, default `100`, max `1000`)
* **Access**: `ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`

#### `POST /api/v2/telemetry/ingest`
Protected ingestion endpoint for Local Gateway offline synchronization.
* **Access**: `ROLE_GATEWAY`, `ROLE_ADMIN` (Rejects unauthenticated callers)
* **Request Body**: Array of `AFES2TelemetryPayload` objects (see `[TELEMETRY_SCHEMA.md](TELEMETRY_SCHEMA.md)`).
* **Response `202 Accepted`**:
  ```json
  {
    "success": true,
    "timestamp": 1794457200000,
    "data": {
      "ingested_count": 50,
      "duplicates_dropped": 0,
      "status": "PROCESSED"
    }
  }
  ```

---

### 4.5. Alarm and Emergency Management

#### `GET /api/v2/alarms/active`
Retrieves all unacknowledged or un-cleared emergency alarms.
* **Access**: `ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`

#### `POST /api/v2/alarms/{alarmId}/acknowledge`
Operator acknowledges an active alarm, silencing sirens while maintaining vigilance.
* **Access**: `ROLE_OPERATOR`, `ROLE_ADMIN`
* **Request Body**:
  ```json
  {
    "note": "Operator dispatched security team to inspect Room 101."
  }
  ```

#### `POST /api/v2/alarms/{alarmId}/resolve`
Marks an alarm event as resolved once physical safety is confirmed.
* **Access**: `ROLE_ADMIN`

---

### 4.6. Actuator Control and Command Dispatch (RPC Facade)

#### `POST /api/v2/control/command`
Dispatches a verified actuator control command to target hardware or virtual nodes.
* **Access**: `ROLE_ADMIN`
* **Request Body**:
  ```json
  {
    "target_device_id": "ESP32S3-YOLO-01",
    "target_zone_id": "ZONE-101",
    "action": "PUMP_ON",
    "parameters": {
      "duration_ms": 10000
    },
    "idempotency_key": "idemp-client-20261112-9941"
  }
  ```
* **Response `200 OK`**:
  ```json
  {
    "success": true,
    "timestamp": 1794457200000,
    "data": {
      "command_id": "cmd-d4b89211-12c8-4712-b13a-96ea9d880401",
      "status": "EXECUTED",
      "execution_duration_ms": 120,
      "message": "Water pump relay energized for 10000 ms"
    }
  }
  ```

#### `POST /api/v2/control/emergency-shutdown`
Broadcast emergency suppression command engaging all suppression outputs across the building.
* **Access**: `ROLE_ADMIN`

#### `POST /api/v2/control/reset`
Issues a synchronized reset command (`RESET_ALERTS`) that safely unlatches alert states and resets output relays after physical confirmation.
* **Access**: `ROLE_ADMIN`

---

### 4.7. Local Gateway & CoreIOT Synchronization

#### `POST /api/v2/gateway/heartbeat`
Reports Local Gateway operational health, interface states, and sync metrics.
* **Access**: `ROLE_GATEWAY`
* **Request Body**:
  ```json
  {
    "gateway_id": "GW-LOCAL-PC01",
    "software_version": "2.0.0-gateway",
    "connected_nodes": 4,
    "interfaces": {
      "esp_now": "HEALTHY",
      "modbus_rs485": "HEALTHY",
      "ble": "IDLE"
    },
    "buffered_packets_count": 0,
    "coreiot_sync_status": "CONNECTED"
  }
  ```

---

### 4.8. Stage A Simulation Control Endpoints

These endpoints operate only when `is_simulated = true` is enabled in configuration, allowing verification of the full pipeline before Stage B hardware arrives.

#### `POST /api/v2/simulation/scenario/start`
Injects synthetic environmental anomalies (e.g., thermal spike, rapid smoke progression, sensor offline fault).
* **Access**: `ROLE_ADMIN`
* **Request Body**:
  ```json
  {
    "scenario_id": "SMOKE_AND_FLAME_BURST",
    "target_zone_id": "ZONE-101",
    "parameters": {
      "initial_temp_c": 28.0,
      "peak_temp_c": 75.0,
      "peak_smoke_ppm": 950.0,
      "duration_seconds": 60,
      "inject_flame_detection": true
    }
  }
  ```

#### `POST /api/v2/simulation/scenario/stop`
Terminates active simulation scenario and restores baseline synthetic data generation.
* **Access**: `ROLE_ADMIN`

---

## 5. WebSocket Real-Time Stream Specification

Real-time telemetry and alarm notifications are pushed to frontend clients via STOMP over WebSocket at `/ws/v2/stream`.

### 5.1. Connection Handshake
1. Client establishes WebSocket connection with header:
   ```http
   Authorization: Bearer <jwt_access_token>
   ```
2. Client sends STOMP `CONNECT` frame. Server validates JWT claims.

### 5.2. Subscription Topics

| Destination | Role Required | Description |
|---|---|---|
| `/topic/zones/all/summary` | `ROLE_VIEWER`+ | Broadcasts 1 Hz summary updates for the dashboard. |
| `/topic/zones/{zoneId}/telemetry` | `ROLE_VIEWER`+ | Live raw telemetry stream for a specific monitored zone. |
| `/topic/alarms` | `ROLE_OPERATOR`+ | Immediate push of critical fire and smoke alarm events. |
| `/topic/devices/{deviceId}/status` | `ROLE_OPERATOR`+ | Real-time device connection state transitions. |
