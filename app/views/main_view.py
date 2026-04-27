import tkinter as tk
from tkinter import ttk
from typing import Callable

from app.assets import Theme
from app.views.clock_view import ClockView
from app.views.alarm_view import AlarmView

TIMEZONES = [
    "America/Bogota",
    "America/New_York",
    "America/Los_Angeles",
    "America/Mexico_City",
    "America/Santiago",
    "America/Sao_Paulo",
    "Europe/Madrid",
    "Europe/London",
    "Asia/Tokyo",
    "Asia/Shanghai",
]


class MainView:
    def __init__(self,
                 on_zone: Callable,
                 on_add_alarm: Callable,
                 on_delete_alarm: Callable,
                 on_toggle_theme: Callable):

        self._theme = Theme.LIGHT
        self._dark_mode = False

        self.root = tk.Tk()
        self.root.title("Reloj Analógico")
        self.root.resizable(False, False)
        self.root.configure(bg=self._theme["bg"])

        self._on_zone = on_zone
        self._on_toggle_theme = on_toggle_theme

        self._main = tk.Frame(self.root, bg=self._theme["bg"])
        self._main.pack(fill="both", expand=True, padx=16, pady=10)

        self._build_header()
        self._build_zone_selector()
        self._build_clock()
        self._build_time_labels()
        self._build_divider()

        self._alarm_view = AlarmView(
            self._main, self._theme,
            on_add=on_add_alarm,
            on_delete=on_delete_alarm,
        )

        self._build_theme_button()

    def _build_header(self):
        t = self._theme
        self._frm_header = tk.Frame(self._main, bg=t["btn_bg"], pady=8)
        self._frm_header.pack(fill="x", pady=(0, 6))
        self._lbl_title = tk.Label(
            self._frm_header, text="⏱  Reloj Analógico",
            font=("Georgia", 17, "bold"),
            bg=t["btn_bg"], fg="#FFFFFF",
        )
        self._lbl_title.pack()

    def _build_zone_selector(self):
        t = self._theme
        self._frm_zone = tk.Frame(self._main, bg=t["bg"])
        self._frm_zone.pack(pady=4)
        self._lbl_zone = tk.Label(
            self._frm_zone, text="Zona horaria:",
            bg=t["bg"], fg=t["subtext"], font=("Helvetica", 9),
        )
        self._lbl_zone.pack(side="left", padx=4)
        self._var_zone = tk.StringVar(value=TIMEZONES[0])
        self._combo_zone = ttk.Combobox(
            self._frm_zone, values=TIMEZONES,
            textvariable=self._var_zone, state="readonly", width=24,
        )
        self._combo_zone.pack(side="left")
        self._combo_zone.bind("<<ComboboxSelected>>",
                              lambda _: self._on_zone(self._var_zone.get()))

    def _build_clock(self):
        self._clock_view = ClockView(self._main, self._theme)

    def _build_time_labels(self):
        t = self._theme
        self._lbl_time = tk.Label(
            self._main, text="00:00:00",
            font=("Courier New", 20, "bold"),
            bg=t["bg"], fg=t["accent"],
        )
        self._lbl_time.pack()
        self._lbl_date = tk.Label(
            self._main, text="",
            font=("Helvetica", 10),
            bg=t["bg"], fg=t["subtext"],
        )
        self._lbl_date.pack()

    def _build_divider(self):
        t = self._theme
        self._frm_divider = tk.Frame(self._main, bg=t["panel_border"], height=1)
        self._frm_divider.pack(fill="x", pady=8)
        self._lbl_alarm_title = tk.Label(
            self._main, text="🔔  Alarmas",
            font=("Helvetica", 11, "bold"),
            bg=t["bg"], fg=t["text"],
        )
        self._lbl_alarm_title.pack(anchor="w", padx=6)

    def _build_theme_button(self):
        t = self._theme
        self._btn_theme = tk.Button(
            self._main, text="🌙  Modo Oscuro",
            command=self._on_toggle_theme,
            bg=t["btn_bg"], fg=t["btn_fg"],
            font=("Helvetica", 9, "bold"),
            relief="flat", padx=12, pady=5, cursor="hand2",
            activebackground=t["btn_bg"], activeforeground=t["btn_fg"],
        )
        self._btn_theme.pack(pady=8)

    # ── Public API ────────────────────────────────
    def update_clock(self, hour, minute, second, microsecond):
        self._clock_view.draw(hour, minute, second, microsecond)

    def update_time_text(self, time_str: str, date_str: str):
        self._lbl_time.config(text=time_str)
        self._lbl_date.config(text=date_str)

    def refresh_alarms(self, alarms: list):
        self._alarm_view.refresh_list(alarms)

    def get_alarm_input(self):
        return (
            self._alarm_view.get_hour(),
            self._alarm_view.get_minute(),
            self._alarm_view.get_label(),
        )

    def get_alarm_selection(self):
        return self._alarm_view.get_selection()

    def toggle_theme(self):
        self._dark_mode = not self._dark_mode
        self._theme = Theme.DARK if self._dark_mode else Theme.LIGHT
        self._btn_theme.config(
            text="☀️  Modo Claro" if self._dark_mode else "🌙  Modo Oscuro"
        )
        self._apply_theme()

    def _apply_theme(self):
        t = self._theme
        self.root.configure(bg=t["bg"])
        self._main.config(bg=t["bg"])
        self._frm_header.config(bg=t["btn_bg"])
        self._lbl_title.config(bg=t["btn_bg"], fg="#FFFFFF")
        self._frm_zone.config(bg=t["bg"])
        self._lbl_zone.config(bg=t["bg"], fg=t["subtext"])
        self._lbl_time.config(bg=t["bg"], fg=t["accent"])
        self._lbl_date.config(bg=t["bg"], fg=t["subtext"])
        self._frm_divider.config(bg=t["panel_border"])
        self._lbl_alarm_title.config(bg=t["bg"], fg=t["text"])
        self._btn_theme.config(
            bg=t["btn_bg"], fg=t["btn_fg"],
            activebackground=t["btn_bg"], activeforeground=t["btn_fg"],
        )
        self._clock_view.apply_theme(t)
        self._alarm_view.apply_theme(t)

        # Update ttk Combobox colors
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=t["input_bg"],
                        background=t["btn_bg"],
                        foreground=t["input_fg"],
                        selectbackground=t["accent"],
                        selectforeground="#FFFFFF",
                        bordercolor=t["panel_border"],
                        arrowcolor=t["btn_fg"])

    def start(self):
        self.root.mainloop()
