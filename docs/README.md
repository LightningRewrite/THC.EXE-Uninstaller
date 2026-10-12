# THC.EXE Uninstaller — PWA prototype

A standalone, installable browser edition. This is a *functional reimplementation* from the Windows app feature documentation, **not** a direct port of its Python source or JSON schema.

## Features
- 16 THC-free hourly checkboxes (8 AM–11 PM)
- Craving occurred / craving passed events with optional trigger notes
- Review and edit historical checkpoints
- All-time totals, two simple analytics charts, checked-hour milestones
- Offline operation after first successful load
- Device-local data and PWA JSON export/import backups
- No lapse/failure tracking by design

## Run locally

```sh
cd THC_EXE_PWA
python -m http.server 8000
```

Open http://localhost:8000 in your browser. **Do not open `index.html` with `file://`**; the service worker requires localhost or HTTPS.

## Publish with GitHub Pages

1. Create a public repository for this PWA (or add these files under a dedicated published folder).
2. Upload the **contents** of this directory to the root of the repository, including `index.html`, `sw.js`, `manifest.webmanifest`, `icons/`, and assets.
3. In repository **Settings → Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, then Save.
4. Wait for the generated HTTPS URL to become available; open it and refresh once. Use your browser's Install or Add to Home Screen option.

On subsequent releases, increase the `CACHE` version in `sw.js` so users load your latest assets. `start_url` and scope are relative, so project-site URLs work.

## Important differences / risks

- **Does not import the existing Windows JSON files.** PWA backups are a different format. A schema adapter requires samples of the actual Python JSON structure.
- **No syncing between devices.** Browser localStorage is scoped to the specific browser and URL. Clearing site data or private browsing can erase history; export regular backups.
- If the user opens both a GitHub Pages URL and localhost, those are **separate** data stores.
- Installing does not automatically migrate records from the Windows desktop application.
- Milestones are counted from **checked hours**; unchecked hours do not mean use or failure.
- Do not publish any personal recovery log files in your source repository.
- This tool is self-monitoring software, not a medically validated treatment.
