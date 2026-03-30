#!/usr/bin/env python3
"""
Practice 5 — TCP client + sliders.
Connects to server.py and sends  servoid,position  lines in real time (debounced).
"""

import socket
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Dict, Optional

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5005
SERVO_IDS = (1, 2, 3, 4)
DEBOUNCE_MS = 45


class ServoSliderClient:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Practice 5 — Client (sliders)")
        self.root.minsize(440, 320)

        self.sock: Optional[socket.socket] = None
        self.pending_after: Dict[int, Optional[str]] = {i: None for i in SERVO_IDS}
        self.scales: Dict[int, tk.Scale] = {}

        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Host:").grid(row=0, column=0, sticky=tk.W)
        self.host_var = tk.StringVar(value=DEFAULT_HOST)
        ttk.Entry(top, textvariable=self.host_var, width=16).grid(row=0, column=1, padx=4)
        ttk.Label(top, text="Port:").grid(row=0, column=2, sticky=tk.W)
        self.port_var = tk.StringVar(value=str(DEFAULT_PORT))
        ttk.Entry(top, textvariable=self.port_var, width=8).grid(row=0, column=3, padx=4)
        self.btn_conn = ttk.Button(top, text="Connect", command=self.toggle_connect)
        self.btn_conn.grid(row=0, column=4, padx=8)

        sliders = ttk.LabelFrame(self.root, text="Servo positions (0–180)", padding=10)
        sliders.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        for idx, sid in enumerate(SERVO_IDS):
            row = ttk.Frame(sliders)
            row.pack(fill=tk.X, pady=4)
            ttk.Label(row, text=f"Servo {sid}", width=10).pack(side=tk.LEFT)
            val_var = tk.IntVar(value=90)
            scale = tk.Scale(
                row,
                from_=0,
                to=180,
                orient=tk.HORIZONTAL,
                length=280,
                variable=val_var,
                command=self._make_slider_cmd(sid),
            )
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
            lbl = ttk.Label(row, text="90", width=4)
            lbl.pack(side=tk.LEFT)
            val_var.trace_add("write", lambda *_a, s=sid, v=val_var, l=lbl: l.configure(text=str(v.get())))
            self.scales[sid] = scale

        ttk.Label(
            self.root,
            text="Move sliders — commands are sent over TCP to the server (debounced for serial).",
            wraplength=400,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=8, pady=(0, 8))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _make_slider_cmd(self, servo_id: int) -> Callable[[str], None]:
        def _on_move(_value: str) -> None:
            self._schedule_send(servo_id)

        return _on_move

    def _schedule_send(self, servo_id: int) -> None:
        aid = self.pending_after.get(servo_id)
        if aid is not None:
            self.root.after_cancel(aid)
        self.pending_after[servo_id] = self.root.after(
            DEBOUNCE_MS, lambda: self._flush_send(servo_id)
        )

    def _flush_send(self, servo_id: int) -> None:
        self.pending_after[servo_id] = None
        if self.sock is None:
            return
        scale = self.scales.get(servo_id)
        if scale is None:
            return
        pos = int(float(scale.get()))
        pos = max(0, min(180, pos))
        line = f"{servo_id},{pos}\n"
        try:
            self.sock.sendall(line.encode("ascii"))
        except OSError as e:
            messagebox.showerror("Send", str(e))
            self.disconnect()

    def toggle_connect(self) -> None:
        if self.sock is not None:
            self.disconnect()
            return
        host = self.host_var.get().strip()
        if not host:
            messagebox.showwarning("Host", "Enter server host.")
            return
        try:
            port = int(self.port_var.get())
        except ValueError:
            messagebox.showerror("Port", "Port must be an integer.")
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
        except OSError as e:
            messagebox.showerror("Connect", str(e))
            s.close()
            return
        self.sock = s
        self.btn_conn.configure(text="Disconnect")
        for sid in SERVO_IDS:
            self._flush_send(sid)

    def disconnect(self) -> None:
        for sid in SERVO_IDS:
            aid = self.pending_after.get(sid)
            if aid is not None:
                try:
                    self.root.after_cancel(aid)
                except tk.TclError:
                    pass
                self.pending_after[sid] = None
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None
        self.btn_conn.configure(text="Connect")

    def on_close(self) -> None:
        self.disconnect()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    ServoSliderClient().run()


if __name__ == "__main__":
    main()
