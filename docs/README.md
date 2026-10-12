# THC.EXE Uninstaller — Browser / PWA

This is a **static, offline-capable PWA** port of the included desktop Tkinter tracker. There is **no hosted database, no API, and no Python requirement for users**. All records are saved in the browser's local storage.

## Publish for everyone to use

1. Push the `docs/` directory to your GitHub repository.
2. Go to **Settings → Pages → Build and deployment**.
3. Select **Deploy from a branch**, `main`, and `/docs`. Save.
4. Visit the GitHub Pages URL shown there. Users can start instantly and optionally install the PWA using Chrome or Edge's install menu.

## Test locally

From `docs/`, run `py -m http.server 8000`, then visit `http://localhost:8000`. This Python command is **only a development web server**; visitors to GitHub Pages do not need Python.

## Data compatibility

- Import your desktop `~/.thc_exe_uninstaller/abstinence_log.json` with **Data & privacy → Import existing JSON**.
- Export browser data to JSON to make backups and move data between versions.
- Import replaces the PWA's browser-local copy *only after confirmation*.
- Clearing browser data can erase local saves. Export backups regularly.

## Scope

The tracker, 8 AM–11 PM checkpoints, eligibility guard, cravings, passed cravings, history corrections, and event types are ported from `thc_exe_uninstaller.py`. Browser analytics presents event counts and checkpoint summaries. The original desktop `analytics.window` module is absent from the supplied ZIP, so this PWA **does not claim to reproduce that window's exact graphs or calculations**. Neither version automatically synchronizes data.
