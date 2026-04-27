import math
import tkinter as tk

from app.utils import TimeUtils


class ClockView:
    RADIUS = 160
    CX = CY = 190

    def __init__(self, parent: tk.Widget, theme: dict):
        self._theme = theme
        self.canvas = tk.Canvas(
            parent, width=380, height=380,
            bg=theme["bg"], highlightthickness=0,
        )
        self.canvas.pack(pady=6)

    def apply_theme(self, theme: dict) -> None:
        self._theme = theme
        self.canvas.config(bg=theme["bg"])

    def draw(self, hour: int, minute: int, second: int, microsecond: int = 0) -> None:
        self.canvas.delete("all")
        t = self._theme
        cx, cy, r = self.CX, self.CY, self.RADIUS

        self._draw_face(cx, cy, r, t)
        self._draw_ticks_and_numbers(cx, cy, r, t)
        self._draw_second_hand(cx, cy, r, t, second, microsecond)
        self._draw_minute_hand(cx, cy, r, t, minute, second)
        self._draw_hour_hand(cx, cy, r, t, hour, minute)
        self._draw_pivot(cx, cy, t)

    def _draw_face(self, cx, cy, r, t):
        self.canvas.create_oval(
            cx - r + 7, cy - r + 7, cx + r + 7, cy + r + 7,
            fill=t["shadow"], outline=""
        )
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=t["clock_face"], outline=t["clock_border"], width=4
        )
        self.canvas.create_oval(
            cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12,
            outline=t["tick_min"], width=1, fill=""
        )

    def _draw_ticks_and_numbers(self, cx, cy, r, t):
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                r_out, r_in, width, color = r - 2, r - 20, 2.5, t["tick_hour"]
            else:
                r_out, r_in, width, color = r - 10, r - 18, 1.0, t["tick_min"]
            self.canvas.create_line(
                cx + r_in * math.cos(angle), cy + r_in * math.sin(angle),
                cx + r_out * math.cos(angle), cy + r_out * math.sin(angle),
                fill=color, width=width, capstyle=tk.ROUND
            )
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            self.canvas.create_text(
                cx + (r - 38) * math.cos(angle),
                cy + (r - 38) * math.sin(angle),
                text=str(i), fill=t["numbers"],
                font=("Georgia", 12, "bold")
            )

    def _draw_second_hand(self, cx, cy, r, t, second, microsecond):
        sec = second + microsecond / 1_000_000
        angle = TimeUtils.second_angle(sec)
        sx, sy = TimeUtils.point(cx, cy, angle, r - 22)
        cx2, cy2 = TimeUtils.point(cx, cy, angle + math.pi, 28)
        self.canvas.create_line(cx2, cy2, sx, sy,
                                fill=t["hand_sec"], width=2, capstyle=tk.ROUND)
        self.canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4,
                                fill=t["hand_sec"], outline="")

    def _draw_minute_hand(self, cx, cy, r, t, minute, second):
        angle = TimeUtils.minute_angle(minute, second)
        mx, my = TimeUtils.point(cx, cy, angle, r - 38)
        self._draw_hand_polygon(cx, cy, mx, my, t["hand_min"], width=5)

    def _draw_hour_hand(self, cx, cy, r, t, hour, minute):
        angle = TimeUtils.hour_angle(hour, minute)
        hx, hy = TimeUtils.point(cx, cy, angle, r - 68)
        self._draw_hand_polygon(cx, cy, hx, hy, t["hand_hour"], width=8)

    def _draw_pivot(self, cx, cy, t):
        self.canvas.create_oval(
            cx - 9, cy - 9, cx + 9, cy + 9,
            fill=t["pivot"], outline=t["clock_face"], width=2
        )

    def _draw_hand_polygon(self, cx, cy, x, y, color, width):
        length = math.hypot(x - cx, y - cy)
        if length == 0:
            return
        px = -(y - cy) / length * width / 2
        py =  (x - cx) / length * width / 2
        pts = [
            cx + px * 0.5, cy + py * 0.5,
            cx + px * 0.2, cy + py * 0.2,
            x  + px * 0.1, y  + py * 0.1,
            x  - px * 0.1, y  - py * 0.1,
            cx - px * 0.2, cy - py * 0.2,
            cx - px * 0.5, cy - py * 0.5,
        ]
        self.canvas.create_polygon(pts, fill=color, outline=color, smooth=True)
