## v1.1.2 [2026-08-28]

- Fix Docker build failing outside the HA builder: default BUILD_FROM, handle PEP 668
  externally-managed-environment when installing pip packages

## v1.1.1 [2026-08-28]

- Remove unused import
- Retry MQTT connection at startup instead of crashing if broker is not yet available

## v1.1.0 [2026-08-28]

- Fix misspelled changelog filename (CHANGELONG -> CHANGELOG)
- Pin dependency versions for reproducible builds
- Make MQTT credentials configurable via add-on options
- Add robustness: configurable topic, offline handling, per-message error logging

## v1.0.2 [2000-01-01]

- Added working addon
