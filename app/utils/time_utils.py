import math
import datetime
from zoneinfo import ZoneInfo


class TimeUtils:
    @staticmethod
    def now_in_zone(zone: str) -> datetime.datetime:
        return datetime.datetime.now(ZoneInfo(zone))

    @staticmethod
    def second_angle(sec: float) -> float:
        return math.radians(sec * 6 - 90)

    @staticmethod
    def minute_angle(min_: float, sec: float) -> float:
        return math.radians((min_ + sec / 60) * 6 - 90)

    @staticmethod
    def hour_angle(hour: float, min_: float) -> float:
        return math.radians((hour % 12 + min_ / 60) * 30 - 90)

    @staticmethod
    def point(cx: float, cy: float, angle: float, length: float):
        return (cx + length * math.cos(angle), cy + length * math.sin(angle))
