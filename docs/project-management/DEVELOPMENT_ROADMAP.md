# IoT-first development roadmap

Dates are set by the team; sequence and gates are fixed by dependencies.

## Milestone 0 — Scope alignment

- Remove archived-only active paths.
- Publish consistent architecture, ownership, status, and evidence rules.
- Gate: active internal links resolve and hygiene CI passes.

## Milestone 1 — Gateway and onboarding

- T08 Local Gateway [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7), owned by Khánh.
- Secure CoreIOT onboarding [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3), owned by Huy.
- Gate: simulator → gateway validation/forwarding works; credentials remain out of Git.

## Milestone 2 — Native CoreIOT operations

- T11 native dashboard [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33), owned by Ý.
- T12/T13 RuleChain and alarms [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34), owned by Huy.
- Gate: sanitized exports import successfully; widget, trigger, no-trigger, and alarm-lifecycle evidence is labelled `SIMULATION` unless physical input is actually used.

## Milestone 3 — Synchronization

- T15 [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35), owned jointly by Huy and Khánh.
- Gate: disconnect/reconnect, ordered replay, deduplication, health, and authorized command round trip pass.

## Milestone 4 — Physical foundation when available

- ESP32-S3 PlatformIO foundation [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36), owned by Khánh.
- Gate: reproducible build plus physical flash, boot, and MQTT evidence.

T01–T07, T09, T14, and N01–N07 remain deferred. T10 is only a minimal CLI/health endpoint and not a score claim. See [IOT_FIRST_SCOPE.md](IOT_FIRST_SCOPE.md).
