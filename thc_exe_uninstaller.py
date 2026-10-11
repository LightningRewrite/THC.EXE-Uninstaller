#!/usr/bin/env python3
"""THC.EXE Uninstaller: local, offline cannabis-abstinence tracker (Tkinter)."""
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from pathlib import Path
import sys

APP_DIR = Path.home() / '.thc_exe_uninstaller'
LEGACY_APP_DIR = Path.home() / '.thoros'  # Previous release's local data folder
LOG_PATH = APP_DIR / 'abstinence_log.json'
HOURS = list(range(8, 24))  # 8 AM through 11 PM, 16 checkboxes


def resource_path(name: str) -> Path:
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
    return base / name


def apply_window_icon(window):
    icon_path = resource_path('thc_exe_uninstaller.ico')
    try:
        if icon_path.exists():
            window.iconbitmap(default=str(icon_path))
    except Exception:
        pass



def migrate_legacy_data():
    """Copy previous-version records without overwriting existing records."""
    if not LEGACY_APP_DIR.is_dir():
        return
    for filename in ('abstinence_log.json', 'recovery_telemetry_extras.json'):
        old = LEGACY_APP_DIR / filename
        new = APP_DIR / filename
        if not old.is_file() or new.exists():
            continue
        APP_DIR.mkdir(parents=True, exist_ok=True)
        # exclusive create prevents accidental replacement of records
        with old.open('rb') as source, new.open('xb') as dest:
            shutil.copyfileobj(source, dest)


def load_data():
    try:
        data = json.loads(LOG_PATH.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('Invalid data')
        return data
    except FileNotFoundError:
        return {'days': {}, 'events': []}
    except (ValueError, OSError) as exc:
        messagebox.showwarning('Log could not be loaded', f'{exc}\nA fresh session will be shown; existing file will not be overwritten until you make a change.')
        return None


def save_data(data):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = LOG_PATH.with_suffix('.tmp')
    temp_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    temp_path.replace(LOG_PATH)


class THCExeUninstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('THC.EXE Uninstaller')
        self.geometry('750x670')
        self.minsize(650, 590)
        self.configure(bg='#111827')
        apply_window_icon(self)
        try:
            migrate_legacy_data()
        except OSError as exc:
            messagebox.showwarning('Existing data migration',
                f'Could not copy old recovery records: {exc}\nThe previous files remain unchanged.')
        self.data = load_data()
        self.readonly = self.data is None
        if self.readonly:
            self.data = {'days': {}, 'events': []}
        self.day = date.today().isoformat()
        self.check_vars = {}
        self.analytics_window = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.build_menu()
        self.build_ui()
        self.load_day()
        self.update_stats()

    def record(self, kind, detail=''):
        if self.readonly:
            messagebox.showerror('Read-only', 'Existing log could not be loaded. Repair or back up the JSON file first.')
            return False
        entry = {'at': datetime.now().astimezone().isoformat(timespec='seconds'), 'type': kind, 'detail': detail}
        self.data.setdefault('events', []).append(entry)
        try:
            save_data(self.data)
        except OSError as exc:
            self.data['events'].pop()
            messagebox.showerror('Save failed', str(exc))
            return False
        self.refresh_events()
        return True

    def build_menu(self):
        menubar = tk.Menu(self)
        logs_menu = tk.Menu(menubar, tearoff=0)
        logs_menu.add_command(label='Browse / Edit Days...', command=self.open_logs)
        menubar.add_cascade(label='Logs', menu=logs_menu)
        menubar.add_command(label='Analytics', command=self.open_analytics)
        self.config(menu=menubar)

    def open_analytics(self):
        """Open native offline Tkinter analytics; no network service."""
        try:
            from analytics.window import AnalyticsWindow
            if self.analytics_window is not None and self.analytics_window.winfo_exists():
                self.analytics_window.lift()
                self.analytics_window.focus_force()
                return
            self.analytics_window = AnalyticsWindow(self, LOG_PATH)
        except (OSError, ImportError, ValueError, tk.TclError) as exc:
            messagebox.showerror('Analytics unavailable', str(exc), parent=self)

    def on_close(self):
        self.destroy()

    def open_logs(self):
        """Review and amend checkpoint history, without deleting audit events."""
        if getattr(self, 'logs_window', None) and self.logs_window.winfo_exists():
            self.logs_window.lift()
            self.logs_window.focus_force()
            return

        win = tk.Toplevel(self)
        self.logs_window = win
        win.title('THC.EXE Uninstaller | Logs')
        win.geometry('735x600')
        win.minsize(650, 490)
        win.configure(bg='#111827')
        apply_window_icon(win)
        win.transient(self)

        main = tk.Frame(win, bg='#111827', padx=20, pady=16)
        main.pack(fill='both', expand=True)
        tk.Label(main, text='ABSTINENCE.LOG  //  HISTORY', bg='#111827',
                 fg='#93c5fd', font=('Consolas', 17, 'bold')).pack(anchor='w')
        tk.Label(main, text='Select a date to review or correct its completed checkpoints.',
                 bg='#111827', fg='#cbd5e1', font=('Segoe UI', 10)).pack(anchor='w', pady=(4, 14))

        nav = tk.Frame(main, bg='#111827')
        nav.pack(fill='x')
        selected = tk.StringVar(value=self.day)
        date_options = sorted(set(self.data.get('days', {})) | {self.day}, reverse=True)
        tk.Label(nav, text='DATE (YYYY-MM-DD)', bg='#111827', fg='#e5e7eb').pack(side='left', padx=(0, 8))
        picker = ttk.Combobox(nav, textvariable=selected, values=date_options,
                              width=15)
        picker.pack(side='left', padx=(0, 8))
        summary = tk.Label(main, text='', bg='#111827', fg='#93c5fd',
                           font=('Consolas', 11, 'bold'))

        check_pane = tk.LabelFrame(main, text=' CHECKPOINTS ', bg='#1f2937',
                                   fg='#e5e7eb', font=('Consolas', 11, 'bold'),
                                   padx=12, pady=12)
        history_vars = {}
        day_label = tk.Label(check_pane, text='', bg='#1f2937', fg='#d1d5db')
        day_label.pack(anchor='w', pady=(0, 10))
        check_grid = tk.Frame(check_pane, bg='#1f2937')
        check_grid.pack(fill='x')

        event_pane = tk.LabelFrame(main, text=' EVENTS FOR SELECTED DAY ',
                                   bg='#1f2937', fg='#e5e7eb', font=('Consolas', 11, 'bold'),
                                   padx=10, pady=8)
        events = tk.Text(event_pane, bg='#0b1220', fg='#cbd5e1',
                         font=('Consolas', 9), wrap='word', relief='flat', state='disabled')
        events.pack(fill='both', expand=True)
        status = tk.Label(main, text='Corrections are saved immediately and recorded in the event log.',
                          bg='#111827', fg='#9ca3af', font=('Segoe UI', 9), wraplength=650)

        def parse_selected(show_error=True):
            try:
                value = date.fromisoformat(selected.get().strip())
                if value > date.today():
                    raise ValueError('Future dates cannot be edited.')
                return value
            except ValueError as exc:
                if show_error:
                    messagebox.showerror('Invalid date',
                        f'Enter a valid date on or before today in YYYY-MM-DD format.\n{exc}', parent=win)
                return None

        def render():
            day = parse_selected()
            if day is None:
                return
            key = day.isoformat()
            selected.set(key)
            checks = set(self.data.get('days', {}).get(key, []))
            day_label.config(text=day.strftime('%A, %B %d, %Y'))
            for hour, var in history_vars.items():
                var.set(hour in checks)
            summary.config(text=f'CHECKPOINTS COMPLETE: {len(checks)}/16')
            items = [e for e in self.data.get('events', [])
                     if str(e.get('at', ''))[:10] == key or
                     (str(e.get('type', '')).startswith('HISTORY_') and
                      str(e.get('detail', '')).startswith(key + ' '))]
            lines = [f'[{str(e.get("at", ""))[:19].replace("T", " ")}] '
                     f'{e.get("type", "EVENT")}  {e.get("detail", "")}'
                     for e in reversed(items)]
            events.config(state='normal')
            events.delete('1.0', 'end')
            events.insert('end', '\n'.join(lines) or 'No events recorded for this day.')
            events.config(state='disabled')
            status.config(text='Corrections are saved immediately and recorded in the event log.')

        def change_hour(hour):
            day = parse_selected()
            if day is None:
                render()
                return
            now = datetime.now()
            if day == now.date() and hour >= now.hour:
                # Current-hour and future-hour checkpoints must be completed first.
                if hour > now.hour or now.minute < 59:
                    messagebox.showinfo('Checkpoint not complete',
                        'You can mark a checkpoint only after its hour has finished.', parent=win)
                    render()
                    return
            if self.readonly:
                messagebox.showerror('Read-only', 'Repair or back up the log file before editing.', parent=win)
                render()
                return
            key = day.isoformat()
            checked = set(self.data.setdefault('days', {}).get(key, []))
            previous = sorted(checked)
            marking = history_vars[hour].get()
            if marking:
                checked.add(hour)
            else:
                checked.discard(hour)
            self.data['days'][key] = sorted(checked)
            event = ('HISTORY_CHECKPOINT_COMPLETE' if marking else 'HISTORY_CHECKPOINT_UNMARKED')
            if not self.record(event, f'{key} {hour:02d}:00'):
                if previous:
                    self.data['days'][key] = previous
                else:
                    self.data['days'].pop(key, None)
                render()
                return
            if key == self.day:
                self.load_day()
                self.update_stats()
            render()
            status.config(text=f'Saved correction for {key}, {hour:02d}:00.', fg='#86efac')

        for i, hour in enumerate(HOURS):
            var = tk.BooleanVar()
            history_vars[hour] = var
            label = datetime.strptime(str(hour), '%H').strftime('%I %p').lstrip('0')
            ttk.Checkbutton(check_grid, text=label, variable=var,
                            command=lambda h=hour: change_hour(h)).grid(
                                row=i//8, column=i%8, sticky='w', padx=6, pady=8)

        def shift_day(amount):
            current = parse_selected()
            if current is None:
                return
            shifted = current + timedelta(days=amount)
            if shifted <= date.today():
                selected.set(shifted.isoformat())
                render()

        tk.Button(nav, text='◀ Previous', command=lambda: shift_day(-1)).pack(side='left', padx=4)
        tk.Button(nav, text='Next ▶', command=lambda: shift_day(1)).pack(side='left', padx=4)
        tk.Button(nav, text='Go', command=render).pack(side='left', padx=4)
        picker.bind('<<ComboboxSelected>>', lambda _e: render())
        picker.bind('<Return>', lambda _e: render())
        summary.pack(anchor='w', pady=(12, 8))
        check_pane.pack(fill='x', pady=(0, 12))
        event_pane.pack(fill='both', expand=True)
        status.pack(anchor='w', pady=(10, 0))
        render()

    def build_ui(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 10), padding=8)
        style.configure('TCheckbutton', background='#1f2937', foreground='#f9fafb', font=('Segoe UI', 10))
        frame = tk.Frame(self, bg='#111827', padx=22, pady=18)
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text='THC.EXE UNINSTALLER', bg='#111827', fg='#93c5fd', font=('Consolas', 19, 'bold')).pack(anchor='w')
        tk.Label(frame, text='Track actions, cravings, and progress over time.', bg='#111827', fg='#9ca3af', font=('Segoe UI', 10)).pack(anchor='w', pady=(2, 14))

        self.status = tk.Label(frame, text='POLICY: DENY THC EXECUTION  |  STATUS: OPERATIONAL', bg='#064e3b', fg='#d1fae5', padx=12, pady=12, anchor='w', font=('Consolas', 11, 'bold'))
        self.status.pack(fill='x', pady=(0, 12))

        controls = tk.Frame(frame, bg='#111827')
        controls.pack(fill='x', pady=(0, 12))
        tk.Button(controls, text='⚡ CRAVING OCCURRED', font=('Segoe UI', 12, 'bold'), bg='#f59e0b', fg='#111827', command=self.craving, padx=15, pady=10).pack(side='left', fill='x', expand=True, padx=(0, 7))
        tk.Button(controls, text='✓ CRAVING PASSED', font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#052e16', command=self.passed, padx=15, pady=10).pack(side='left', fill='x', expand=True)

        self.hint = tk.Label(frame, text='Craving detected? Log it. Step away from gear, breathe normally, switch activities. No negotiation required.', bg='#111827', fg='#d1d5db', wraplength=680, justify='left', font=('Segoe UI', 10))
        self.hint.pack(anchor='w', pady=(0, 12))

        pane = tk.LabelFrame(frame, text=' ABSTINENCE.LOG  //  TODAY ', bg='#1f2937', fg='#e5e7eb', font=('Consolas', 11, 'bold'), padx=12, pady=10)
        pane.pack(fill='x', pady=(0, 10))
        self.today_label = tk.Label(pane, text='', bg='#1f2937', fg='#d1d5db', font=('Segoe UI', 10))
        self.today_label.pack(anchor='w')
        checks = tk.Frame(pane, bg='#1f2937')
        checks.pack(fill='x', pady=(8, 4))
        for i, hour in enumerate(HOURS):
            var = tk.BooleanVar()
            self.check_vars[hour] = var
            label = datetime.strptime(str(hour), '%H').strftime('%I %p').lstrip('0')
            ttk.Checkbutton(checks, text=label, variable=var, command=lambda h=hour: self.toggle_hour(h)).grid(row=i//8, column=i%8, sticky='w', padx=7, pady=8)
        self.progress = tk.Label(pane, text='', bg='#1f2937', fg='#93c5fd', font=('Consolas', 11, 'bold'))
        self.progress.pack(anchor='w', pady=(5, 0))

        event_pane = tk.LabelFrame(frame, text=' RECENT EVENTS ', bg='#1f2937', fg='#e5e7eb', font=('Consolas', 11, 'bold'), padx=12, pady=8)
        event_pane.pack(fill='both', expand=True)
        self.events_view = tk.Text(event_pane, bg='#0b1220', fg='#cbd5e1', font=('Consolas', 9), height=9, relief='flat', wrap='word', state='disabled')
        self.events_view.pack(fill='both', expand=True)
        self.refresh_events()
        tk.Label(frame, text=f'Offline logs: {LOG_PATH}', bg='#111827', fg='#9ca3af', font=('Segoe UI', 9), wraplength=680).pack(anchor='w', pady=(10, 0))

    def load_day(self):
        checked = self.data.get('days', {}).get(self.day, [])
        for hour, var in self.check_vars.items():
            var.set(hour in checked)
        self.today_label.config(text=date.today().strftime('%A, %B %d, %Y'))

    def update_stats(self):
        count = sum(v.get() for v in self.check_vars.values())
        self.progress.config(text=f'CHECKPOINTS COMPLETE: {count}/16  |  LOGGING: ENABLED')

    def toggle_hour(self, hour):
        if self.readonly:
            self.load_day()
            return
        now = datetime.now()
        if hour > now.hour or (hour == now.hour and now.minute < 59):
            # Hour denotes its start. Allow marking only once the hour has passed.
            self.check_vars[hour].set(False)
            messagebox.showinfo('Checkpoint not complete', 'Mark an hour only after it has finished.')
            return
        checked = set(self.data.setdefault('days', {}).get(self.day, []))
        old_checked = sorted(checked)
        if self.check_vars[hour].get():
            checked.add(hour)
            event_type = 'CHECKPOINT_COMPLETE'
        else:
            checked.discard(hour)
            event_type = 'CHECKPOINT_UNMARKED'
        self.data['days'][self.day] = sorted(checked)
        if not self.record(event_type, f'{hour:02d}:00'):
            self.data['days'][self.day] = old_checked
            self.check_vars[hour].set(not self.check_vars[hour].get())
        self.update_stats()

    def craving(self):
        if self.record('CRAVING_DETECTED', 'Request DENIED by abstinence policy'):
            self.hint.config(text='REQUEST DENIED. Keep the Arizer out of reach. Change rooms, breathe gently, and choose a short alternative activity. You do not need to argue with the urge.')
            self.status.config(text='THC REQUEST: DENIED  |  INTERRUPT LOGGED', bg='#78350f', fg='#fef3c7')

    def passed(self):
        if self.record('CRAVING_PASSED', 'No THC consumed reported'):
            self.hint.config(text='Interrupt resolved. Resume normal operations. One craving handled does not require the next to disappear.')
            self.status.config(text='POLICY: DENY THC EXECUTION  |  STATUS: OPERATIONAL', bg='#064e3b', fg='#d1fae5')

    def refresh_events(self):
        if not hasattr(self, 'events_view'):
            return
        items = self.data.get('events', [])[-14:]
        lines = []
        for e in reversed(items):
            at = e.get('at', '')
            lines.append(f'[{at[:19].replace("T", " ")}] {e.get("type", "EVENT")}  {e.get("detail", "")}')
        self.events_view.config(state='normal')
        self.events_view.delete('1.0', 'end')
        self.events_view.insert('end', '\n'.join(lines) or 'No events yet. Start logging when a craving arrives.')
        self.events_view.config(state='disabled')


if __name__ == '__main__':
    THCExeUninstaller().mainloop()
