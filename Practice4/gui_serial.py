#!/usr/bin/env python3
"""
Small GUI: pick a COM port, connect, send lines as  servoid,position  (e.g. 1,90).
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from typing import Optional

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    raise SystemExit("Install pyserial: pip install -r requirements.txt") from None

DEFAULT_BAUD = 9600


def list_ports() -> list[str]:
    return [p.device for p in serial.tools.list_ports.comports()]


class ServoSerialApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Practice 4 — Serial servo")
        self.root.minsize(420, 360)
        self.ser: Optional[serial.Serial] = None

        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Port:").grid(row=0, column=0, sticky=tk.W)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(top, textvariable=self.port_var, width=22, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=4)
        ttk.Button(top, text="Refresh", command=self.refresh_ports).grid(row=0, column=2, padx=4)

        ttk.Label(top, text="Baud:").grid(row=0, column=3, sticky=tk.W)
        self.baud_var = tk.StringVar(value=str(DEFAULT_BAUD))
        ttk.Entry(top, textvariable=self.baud_var, width=8).grid(row=0, column=4, padx=4)

        self.btn_connect = ttk.Button(top, text="Connect", command=self.toggle_connect)
        self.btn_connect.grid(row=0, column=5, padx=4)

        mid = ttk.Frame(self.root, padding=8)
        mid.pack(fill=tk.X)

        ttk.Label(mid, text="Servo ID:").grid(row=0, column=0, sticky=tk.W)
        self.servo_var = tk.StringVar(value="1")
        ttk.Entry(mid, textvariable=self.servo_var, width=8).grid(row=0, column=1, padx=4)

        ttk.Label(mid, text="Position (0–180):").grid(row=0, column=2, sticky=tk.W, padx=(12, 0))
        self.pos_var = tk.StringVar(value="90")
        ttk.Entry(mid, textvariable=self.pos_var, width=8).grid(row=0, column=3, padx=4)

        ttk.Button(mid, text="Send", command=self.send_command).grid(row=0, column=4, padx=8)

        log_frame = ttk.LabelFrame(self.root, text="Log", padding=8)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.log = scrolledtext.ScrolledText(log_frame, height=14, state=tk.DISABLED, wrap=tk.WORD)
        self.log.pack(fill=tk.BOTH, expand=True)

        hint = (
            "Protocol: one line per command:  servoid,position  (ASCII), newline-terminated.\n"
            "Example: servo 1 to 90° → ID 1, position 90, then Send."
        )
        ttk.Label(self.root, text=hint, wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, padx=8, pady=(0, 8))

        self.refresh_ports()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def log_line(self, msg: str) -> None:
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def refresh_ports(self) -> None:
        ports = list_ports()
        self.port_combo["values"] = ports
        if ports and self.port_var.get() not in ports:
            self.port_var.set(ports[0])
        elif not ports:
            self.port_var.set("")

    def toggle_connect(self) -> None:
        if self.ser is not None and self.ser.is_open:
            self.disconnect()
        else:
            self.connect()

    def connect(self) -> None:
        port = self.port_var.get().strip()
        if not port:
            messagebox.showwarning("Port", "Select a serial port or plug in the device.")
            return
        try:
            baud = int(self.baud_var.get())
        except ValueError:
            messagebox.showerror("Baud", "Baud must be an integer.")
            return
        try:
            self.ser = serial.Serial(port, baud, timeout=0.2)
            self.btn_connect.configure(text="Disconnect")
            self.log_line(f"Connected: {port} @ {baud}")
        except serial.SerialException as e:
            messagebox.showerror("Serial", str(e))

    def disconnect(self) -> None:
        if self.ser is not None:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None
        self.btn_connect.configure(text="Connect")
        self.log_line("Disconnected.")

    def send_command(self) -> None:
        if self.ser is None or not self.ser.is_open:
            messagebox.showwarning("Serial", "Connect to a port first.")
            return
        sid = self.servo_var.get().strip()
        pos = self.pos_var.get().strip()
        if not sid or not pos:
            messagebox.showwarning("Input", "Enter servo ID and position.")
            return
        try:
            pos_i = int(pos)
        except ValueError:
            messagebox.showerror("Position", "Position must be an integer (0–180).")
            return
        if not (0 <= pos_i <= 180):
            messagebox.showwarning("Position", "Use 0–180 for typical hobby servos.")
        line = f"{sid},{pos_i}\n"
        try:
            self.ser.write(line.encode("ascii"))
            self.ser.flush()
            self.log_line(f"Sent: {sid},{pos_i}")
        except serial.SerialException as e:
            messagebox.showerror("Serial", str(e))

    def on_close(self) -> None:
        self.disconnect()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    ServoSerialApp().run()


if __name__ == "__main__":
    main()
