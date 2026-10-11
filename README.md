# THC.EXE Uninstaller

**Turn an overwhelming, deeply personal struggle into a tangible, reachable goal — one hour at a time.**

THC.EXE Uninstaller is a free, offline Windows tracker for people working toward abstinence from cannabis. It breaks the day into small, checkable milestones and gives you a place to record cravings and review your progress.

You don't have to solve the rest of your life today. Focus on the next hour.

## Features

- **16 hourly checkpoints:** Mark THC-free hours from 8:00 AM through 11:00 PM.
- **Craving events:** Use **⚡ CRAVING OCCURRED** when an urge arises and **✓ CRAVING PASSED** when it passes.
- **Editable history:** Review previous days and correct missed or mistaken checkboxes under **Logs → Browse / Edit Days**.
- **Analytics:** View checkpoint summaries, craving activity, trends, events, and optional observations for craving intensity, mood, sleep, triggers, and notes.
- **Manual analytics refresh:** The analytics dashboard loads when opened and updates when you click **↻ Refresh**. It does not refresh on a timer.
- **Offline and local:** No sign-in, application server, or cloud account is required.

## Download and run (Windows)

1. Open the repository's **Releases** page and download the Windows release ZIP.
2. Extract the ZIP to a folder.
3. Double-click **`THC Uninstaller.exe`** (or the `.exe` filename provided in that release).
4. Start checking off completed THC-free hours and logging cravings.

You do **not** need to install Python to use the prebuilt `.exe`.

> Windows may show an **Unknown publisher** or SmartScreen warning for an unsigned executable. Only run downloads from a release you trust. The project source is provided for inspection.

### Running from source

Requires **Python 3** with Tkinter on Windows:

```powershell
py -3 thc_exe_uninstaller.py
```

Or double-click `Launch_THC_EXE_Uninstaller.bat` in the source folder.

## How to use THC.EXE Uninstaller

1. **Complete an hour without THC.** Check the box for that hour. Checking a box records your own report; it does not verify abstinence.
2. **When a craving occurs,** click **CRAVING OCCURRED**. A craving is not a failed checkpoint.
3. **When it passes,** click **CRAVING PASSED**.
4. **Missed a checkbox?** Use the **Logs** menu to revisit and correct earlier days.
5. **Review patterns.** Open **Analytics**, record optional observations, and use **Refresh** whenever you want to update the displayed results.

Craving-button timestamps are log entries; the interval between buttons is **not** necessarily the duration of a craving. Missing checkboxes do not mean cannabis was used.

## Data and privacy

Recovery logs are stored in your Windows user profile:

```text
%USERPROFILE%\.thc_exe_uninstaller\abstinence_log.json
%USERPROFILE%\.thc_exe_uninstaller\recovery_telemetry_extras.json
```

The first file contains checkpoint and event records. The second holds optional analytics observations. The app does not require network connectivity or upload these records to a central service.

**Back up these JSON files before replacing a computer, reinstalling Windows, or deleting application data.** No online backup or synchronization is provided.

If records exist in the earlier `.thoros` data directory, this version attempts to copy them into the new directory without overwriting existing destination files or deleting the originals.

**When reporting bugs, do not post your personal JSON recovery logs publicly.** Remove dates, notes, usernames, and other sensitive information from screenshots or sample files before sharing.

## Build a Windows executable

The source ZIP contains `Build_Windows_EXE.bat` and `thc_exe_uninstaller.ico`.

1. Install Python 3 on Windows 11.
2. Extract the project, keeping `analytics/`, the `.py` files, and `thc_exe_uninstaller.ico` together.
3. Double-click **`Build_Windows_EXE.bat`**.
4. Find the resulting executable in `dist/`.

The script installs or updates **PyInstaller** (internet may be needed for that step), embeds `thc_exe_uninstaller.ico` in the executable, and bundles the icon for the native application windows. It may also create a separately named **Icon Check** executable to diagnose Windows Explorer's icon cache.

The compiled application does not require Python on the recipient's computer.

## Scope and limitations

THC.EXE Uninstaller is a **self-monitoring and accountability tool**, not a validated treatment, diagnosis, or guaranteed cure for cannabis use disorder. It cannot independently determine whether someone has consumed THC, and its charts reflect the information the user enters. Recovery experiences vary; professional support may be useful alongside self-tracking.

## Feedback and issues

Bug reports and feature suggestions are welcome through the repository's **Issues** page. Please describe steps to reproduce the problem and your Windows version, but **do not include personal recovery data**.

## License

No open-source license is included by default. A public repository does **not** automatically grant permission to reuse, redistribute, or modify its source code. Add a `LICENSE` file if you want to grant those rights.
