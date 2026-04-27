import datetime


class Alarm:
    def __init__(self, hour: int, minute: int, label: str = "Alarm"):
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Hour or minute out of range.")
        self.hour = hour
        self.minute = minute
        self.label = label
        self.active: bool = True
        self._triggered: bool = False

    def check(self, now: datetime.datetime) -> bool:
        match = (
            self.active
            and not self._triggered
            and now.hour == self.hour
            and now.minute == self.minute
            and now.second == 0
        )
        if match:
            self._triggered = True
            return True
        if self._triggered and not (now.hour == self.hour and now.minute == self.minute):
            self._triggered = False
        return False

    def __str__(self) -> str:
        status = "✔" if self.active else "✖"
        return f"{status}  {self.label:<14} {self.hour:02d}:{self.minute:02d}"
