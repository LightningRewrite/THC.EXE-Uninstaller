# THC.EXE Uninstaller — PWA Analytics v2

Host these files directly from your repository’s `/docs` directory through GitHub Pages. Replacing the old `/docs` files triggers the service-worker cache update.

## What's new

Four native-inspired analytics tabs: Overview, Cravings, Trends + Observations, and Events. Includes checkpoint heatmap, achievements, streaks, hourly and daily craving counts, pairing totals, recovery observations with charts, trigger notes, and full event history.

Abstinence records continue to use `thc_exe_uninstaller_data_v1` in browser localStorage, preserving previous PWA data. Imported desktop `abstinence_log.json` stays compatible. New observations use a separate localStorage key and are exported to `recovery_telemetry_extras.json` (PWA format).

**Caveat:** The supplied desktop archive omits its `analytics` Python package, so observations' desktop-side JSON structure cannot be fully verified. The PWA exports its own consistent format but may need an adapter to load an existing desktop telemetry file. Charts are based on self-reported logged events; pairing does not imply measured craving duration. Browser storage can be lost, so export both backups.
