import time
import threading
from tkinter import messagebox

from app.models import Alarm
from app.utils import TimeUtils
from app.views import MainView

try:
    import winsound as _ws
    def _beep():
        for _ in range(5):
            _ws.Beep(880, 250)
            time.sleep(0.18)
except ImportError:
    def _beep():
        for _ in range(4):
            print("\a", end="", flush=True)
            time.sleep(0.3)


class AppController:
    def __init__(self):
        self._zone: str = "America/Bogota"
        self._alarms: list[Alarm] = []

        self._view = MainView(
            on_zone=self._set_zone,
            on_add_alarm=self._add_alarm,
            on_delete_alarm=self._delete_alarm,
            on_toggle_theme=self._toggle_theme,
        )
        self._tick()

    def _tick(self):
        now = TimeUtils.now_in_zone(self._zone)

        self._view.update_clock(now.hour, now.minute, now.second, now.microsecond)
        self._view.update_time_text(
            now.strftime("%H:%M:%S"),
            now.strftime("%A, %d de %B de %Y").capitalize(),
        )

        for alarm in self._alarms:
            if alarm.check(now):
                self._fire_alarm(alarm)

        self._view.root.after(16, self._tick)

    def _add_alarm(self):
        try:
            hour, minute, label = self._view.get_alarm_input()
            self._alarms.append(Alarm(hour, minute, label))
            self._view.refresh_alarms(self._alarms)
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))

    def _delete_alarm(self):
        sel = self._view.get_alarm_selection()
        if sel:
            del self._alarms[sel[0]]
            self._view.refresh_alarms(self._alarms)

    def _fire_alarm(self, alarm: Alarm):
        def notify():
            _beep()
            messagebox.showinfo(
                "🔔 Alarma",
                f"{alarm.label}\n{alarm.hour:02d}:{alarm.minute:02d}",
            )
        threading.Thread(target=notify, daemon=True).start()

    def _set_zone(self, zone: str):
        self._zone = zone

    def _toggle_theme(self):
        self._view.toggle_theme()

    def run(self):
        self._view.start()
