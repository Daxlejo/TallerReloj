import tkinter as tk
from typing import Callable


class _Spinner(tk.Frame):

    def __init__(self, parent, min_val: int, max_val: int, theme: dict, **kwargs):
        super().__init__(parent, bg=theme["panel"])
        self._min = min_val
        self._max = max_val
        self._var = tk.StringVar(value=f"{min_val:02d}")

        btn_cfg = dict(
            font=("Helvetica", 7, "bold"),
            relief="flat", bd=0, cursor="hand2", width=2,
            bg=theme["btn_bg"], fg=theme["btn_fg"],
            activebackground=theme["accent"], activeforeground="#FFFFFF",
        )

        self._entry = tk.Entry(
            self, textvariable=self._var, width=3,
            font=("Courier", 11, "bold"), justify="center",
            bg=theme["input_bg"], fg=theme["input_fg"],
            insertbackground=theme["input_fg"],
            relief="flat", bd=0,
        )
        self._entry.grid(row=0, column=0, rowspan=2, padx=(0, 1), ipady=2)

        self._btn_up = tk.Button(self, text="▲", command=self._increment, **btn_cfg)
        self._btn_up.grid(row=0, column=1, sticky="ew")

        self._btn_dn = tk.Button(self, text="▼", command=self._decrement, **btn_cfg)
        self._btn_dn.grid(row=1, column=1, sticky="ew")

    def _increment(self):
        val = (self.get() + 1) % (self._max + 1)
        if val < self._min:
            val = self._min
        self._var.set(f"{val:02d}")

    def _decrement(self):
        val = self.get() - 1
        if val < self._min:
            val = self._max
        self._var.set(f"{val:02d}")

    def get(self) -> int:
        try:
            return max(self._min, min(self._max, int(self._var.get())))
        except ValueError:
            return self._min

    def apply_theme(self, t: dict):
        self.config(bg=t["panel"])
        self._entry.config(bg=t["input_bg"], fg=t["input_fg"],
                           insertbackground=t["input_fg"])
        for btn in (self._btn_up, self._btn_dn):
            btn.config(bg=t["btn_bg"], fg=t["btn_fg"],
                       activebackground=t["accent"], activeforeground="#FFFFFF")


class AlarmView:
    def __init__(self, parent: tk.Widget, theme: dict,
                 on_add: Callable, on_delete: Callable):
        self._on_add = on_add
        self._on_delete = on_delete

        self.frame = tk.Frame(parent, bg=theme["panel"])
        self.frame.pack(fill="x", padx=14, pady=4)

        self._build(theme)

    def _build(self, t: dict):
        row = tk.Frame(self.frame, bg=t["panel"])
        row.pack(pady=8, padx=8)

        def lbl(text):
            return tk.Label(row, text=text, bg=t["panel"],
                            fg=t["text"], font=("Helvetica", 10))

        lbl("Hora:").pack(side="left")
        self._spin_hour = _Spinner(row, 0, 23, t)
        self._spin_hour.pack(side="left", padx=4)

        lbl("Min:").pack(side="left")
        self._spin_min = _Spinner(row, 0, 59, t)
        self._spin_min.pack(side="left", padx=4)

        lbl("Etiqueta:").pack(side="left")
        self._entry = tk.Entry(
            row, width=11, font=("Helvetica", 10),
            bg="#F5EEEE", fg="#030303",
            insertbackground=t["input_fg"], relief="flat",
        )
        self._entry.insert(0, "Alarma")
        self._entry.pack(side="left", padx=4)

        self._btn_add = tk.Button(
            self.frame, text="＋ Agregar alarma",
            command=self._on_add,
            bg=t["accent"], fg="#FFFFFF",
            font=("Helvetica", 9, "bold"),
            relief="flat", padx=10, pady=4, cursor="hand2",
            activebackground=t["accent"],
        )
        self._btn_add.pack(pady=4)

        self._listbox = tk.Listbox(
            self.frame, height=4, font=("Courier", 10),
            bg=t["list_bg"], fg=t["list_fg"],
            selectbackground=t["list_sel"], selectforeground="#FFFFFF",
            relief="flat", bd=0,
            highlightthickness=1,
            highlightcolor=t["panel_border"],
            highlightbackground=t["panel_border"],
        )
        self._listbox.pack(fill="x", padx=10, pady=4)

        self._btn_del = tk.Button(
            self.frame, text="🗑  Eliminar seleccionada",
            command=self._on_delete,
            bg=t["btn_bg"], fg=t["btn_fg"],
            font=("Helvetica", 8, "bold"),
            relief="flat", padx=8, pady=3, cursor="hand2",
            activebackground=t["btn_bg"], activeforeground=t["btn_fg"],
        )
        self._btn_del.pack(pady=(0, 8))

    def get_hour(self) -> int:
        return self._spin_hour.get()

    def get_minute(self) -> int:
        return self._spin_min.get()

    def get_label(self) -> str:
        return self._entry.get().strip() or "Alarma"

    def get_selection(self):
        return self._listbox.curselection()

    def refresh_list(self, alarms: list) -> None:
        self._listbox.delete(0, tk.END)
        for a in alarms:
            self._listbox.insert(tk.END, str(a))

    def apply_theme(self, t: dict) -> None:
        self.frame.config(bg=t["panel"])
        self._colorize_children(self.frame, t)
        self._spin_hour.apply_theme(t)
        self._spin_min.apply_theme(t)
        self._entry.config(bg=t["input_bg"], fg=t["input_fg"],
                           insertbackground=t["input_fg"])
        self._listbox.config(bg=t["list_bg"], fg=t["list_fg"],
                             selectbackground=t["list_sel"],
                             highlightcolor=t["panel_border"],
                             highlightbackground=t["panel_border"])
        self._btn_add.config(bg=t["accent"], fg="#FFFFFF",
                             activebackground=t["accent"])
        self._btn_del.config(bg=t["btn_bg"], fg=t["btn_fg"],
                             activebackground=t["btn_bg"],
                             activeforeground=t["btn_fg"])

    def _colorize_children(self, widget, t: dict):
        for child in widget.winfo_children():
            cls = child.winfo_class()
            if cls == "Frame":
                child.config(bg=t["panel"])
            elif cls == "Label":
                child.config(bg=t["panel"], fg=t["text"])
            self._colorize_children(child, t)
