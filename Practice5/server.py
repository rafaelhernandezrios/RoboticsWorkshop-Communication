#!/usr/bin/env python3
"""
Practice 5 — TCP server + serial forward.
Waits for a client, receives lines  servoid,position  and writes them to the COM port.
"""

import re
import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from typing import Optional

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    raise SystemExit("Install pyserial: pip install -r requirements.txt") from None

DEFAULT_BAUD = 9600
DEFAULT_TCP_PORT = 5005
SERVO_LINE = re.compile(r"^\s*(\d+)\s*,\s*(\d+)\s*$")


def list_ports() -> list[str]:
    return [p.device for p in serial.tools.list_ports.comports()]


class ServoBridgeServer:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Practice 5 — Server (TCP → serial)")
        self.root.minsize(520, 420)

        self.ser: Optional[serial.Serial] = None
        self.listen_sock: Optional[socket.socket] = None
        self.client_conn: Optional[socket.socket] = None
        self.stop_event = threading.Event()
        self.server_thread: Optional[threading.Thread] = None
        self.recv_buffer = ""

        row1 = ttk.Frame(self.root, padding=8)
        row1.pack(fill=tk.X)
        ttk.Label(row1, text="COM:").grid(row=0, column=0, sticky=tk.W)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(row1, textvariable=self.port_var, width=20, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=4)
        ttk.Button(row1, text="Refresh", command=self.refresh_ports).grid(row=0, column=2, padx=4)
        ttk.Label(row1, text="Baud:").grid(row=0, column=3, sticky=tk.W)
        self.baud_var = tk.StringVar(value=str(DEFAULT_BAUD))
        ttk.Entry(row1, textvariable=self.baud_var, width=8).grid(row=0, column=4, padx=4)
        self.btn_serial = ttk.Button(row1, text="Open serial", command=self.toggle_serial)
        self.btn_serial.grid(row=0, column=5, padx=8)

        row2 = ttk.Frame(self.root, padding=8)
        row2.pack(fill=tk.X)
        ttk.Label(row2, text="TCP bind:").grid(row=0, column=0, sticky=tk.W)
        self.bind_host = tk.StringVar(value="0.0.0.0")
        ttk.Entry(row2, textvariable=self.bind_host, width=12).grid(row=0, column=1, padx=4)
        ttk.Label(row2, text="Port:").grid(row=0, column=2, sticky=tk.W)
        self.tcp_port = tk.StringVar(value=str(DEFAULT_TCP_PORT))
        ttk.Entry(row2, textvariable=self.tcp_port, width=8).grid(row=0, column=3, padx=4)
        self.btn_tcp = ttk.Button(row2, text="Start TCP server", command=self.toggle_tcp)
        self.btn_tcp.grid(row=0, column=4, padx=8)

        log_frame = ttk.LabelFrame(self.root, text="Log", padding=8)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        self.log = scrolledtext.ScrolledText(log_frame, height=16, state=tk.DISABLED, wrap=tk.WORD)
        self.log.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            self.root,
            text="Forwards each line servoid,position to serial (same as Practice 4). Run client.py on another machine or same PC.",
            wraplength=480,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=8, pady=(0, 8))

        self.refresh_ports()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def log_line(self, msg: str) -> None:
        def _append() -> None:
            self.log.configure(state=tk.NORMAL)
            self.log.insert(tk.END, msg + "\n")
            self.log.see(tk.END)
            self.log.configure(state=tk.DISABLED)

        self.root.after(0, _append)

    def refresh_ports(self) -> None:
        ports = list_ports()
        self.port_combo["values"] = ports
        if ports and self.port_var.get() not in ports:
            self.port_var.set(ports[0])
        elif not ports:
            self.port_var.set("")

    def toggle_serial(self) -> None:
        if self.ser is not None and self.ser.is_open:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None
            self.btn_serial.configure(text="Open serial")
            self.log_line("Serial closed.")
            return
        port = self.port_var.get().strip()
        if not port:
            messagebox.showwarning("COM", "Select a serial port.")
            return
        try:
            baud = int(self.baud_var.get())
        except ValueError:
            messagebox.showerror("Baud", "Baud must be an integer.")
            return
        try:
            self.ser = serial.Serial(port, baud, timeout=0.2)
            self.btn_serial.configure(text="Close serial")
            self.log_line(f"Serial open: {port} @ {baud}")
        except serial.SerialException as e:
            messagebox.showerror("Serial", str(e))

    def toggle_tcp(self) -> None:
        if self.server_thread is not None:
            self.stop_tcp()
            return
        if self.ser is None or not self.ser.is_open:
            messagebox.showwarning("Serial", "Open the serial port first (Arduino).")
            return
        try:
            port_n = int(self.tcp_port.get())
        except ValueError:
            messagebox.showerror("Port", "TCP port must be an integer.")
            return
        host = self.bind_host.get().strip() or "0.0.0.0"
        self.stop_event.clear()
        try:
            self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listen_sock.bind((host, port_n))
            self.listen_sock.listen(1)
        except OSError as e:
            messagebox.showerror("TCP", str(e))
            if self.listen_sock:
                try:
                    self.listen_sock.close()
                except OSError:
                    pass
                self.listen_sock = None
            return

        self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
        self.server_thread.start()
        self.btn_tcp.configure(text="Stop TCP server")
        self.log_line(f"TCP listening on {host}:{port_n} — start client.py")

    def _server_loop(self) -> None:
        assert self.listen_sock is not None
        self.log_line("Waiting for client...")
        try:
            while not self.stop_event.is_set():
                self.listen_sock.settimeout(0.5)
                try:
                    conn, addr = self.listen_sock.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break
                self.client_conn = conn
                self.log_line(f"Client connected: {addr[0]}:{addr[1]}")
                self._recv_client(conn)
                self.client_conn = None
                try:
                    conn.close()
                except OSError:
                    pass
                self.log_line("Client disconnected.")
                self.recv_buffer = ""
        finally:
            self.log_line("TCP server stopped.")

    def _recv_client(self, conn: socket.socket) -> None:
        while not self.stop_event.is_set():
            try:
                data = conn.recv(4096)
            except OSError:
                break
            if not data:
                break
            self.recv_buffer += data.decode("utf-8", errors="replace")
            while True:
                if "\n" not in self.recv_buffer:
                    break
                line, self.recv_buffer = self.recv_buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                m = SERVO_LINE.match(line)
                if not m:
                    self.log_line(f"Skip bad line: {line!r}")
                    continue
                sid, pos = m.group(1), m.group(2)
                out = f"{sid},{pos}\n"
                try:
                    if self.ser and self.ser.is_open:
                        self.ser.write(out.encode("ascii"))
                        self.ser.flush()
                        self.log_line(f"→ serial: {sid},{pos}")
                except serial.SerialException as e:
                    self.log_line(f"Serial error: {e}")
                    break

    def stop_tcp(self) -> None:
        self.stop_event.set()
        if self.client_conn:
            try:
                self.client_conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.client_conn.close()
            except OSError:
                pass
            self.client_conn = None
        if self.listen_sock:
            try:
                self.listen_sock.close()
            except OSError:
                pass
            self.listen_sock = None
        if self.server_thread:
            self.server_thread.join(timeout=2.0)
            self.server_thread = None
        self.btn_tcp.configure(text="Start TCP server")
        self.log_line("TCP stopped.")

    def on_close(self) -> None:
        self.stop_tcp()
        if self.ser is not None:
            try:
                self.ser.close()
            except Exception:
                pass
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    ServoBridgeServer().run()


if __name__ == "__main__":
    main()
