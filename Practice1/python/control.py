#!/usr/bin/env python3
"""
Control Arduino LED + servo via pyserial.
Usage:
  python control.py                    # uses default port (edit SERIAL_PORT)
  python control.py /dev/cu.usbmodem*  # or pass port as first argument
"""

import argparse
import sys
import time
from typing import Optional

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("Install dependencies: pip install -r requirements.txt")
    sys.exit(1)

# Default: change to your port (macOS often /dev/cu.usbmodem*, Windows COM3, Linux /dev/ttyUSB0)
DEFAULT_BAUD = 9600


def pick_default_port() -> Optional[str]:
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        return None
    # Prefer common USB-serial chips if multiple
    for p in ports:
        desc = (p.description or "") + (p.manufacturer or "")
        if "Arduino" in desc or "CH340" in desc or "CP210" in desc or "FTDI" in desc:
            return p.device
    return ports[0].device


def main() -> None:
    parser = argparse.ArgumentParser(description="LED + servo over serial")
    parser.add_argument(
        "port",
        nargs="?",
        default=None,
        help="Serial port (e.g. /dev/cu.usbmodem1101 or COM3)",
    )
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    args = parser.parse_args()

    port = args.port or pick_default_port()
    if not port:
        print("No serial port found. Connect Arduino and try again.")
        sys.exit(1)

    print(f"Opening {port} @ {args.baud} baud...")
    ser = serial.Serial(port, args.baud, timeout=1)
    time.sleep(2)  # allow Arduino reset after opening port

    def send(cmd: str) -> None:
        line = cmd if cmd.endswith("\n") else cmd + "\n"
        ser.write(line.encode("ascii"))
        ser.flush()
        if ser.in_waiting:
            print(ser.read(ser.in_waiting).decode("utf-8", errors="replace").strip())

    print("Blink LED, then sweep servo...")
    send("L1")
    time.sleep(0.5)
    send("L0")
    time.sleep(0.5)
    send("L1")
    time.sleep(0.3)
    send("L0")

    for a in (0, 45, 90, 135, 180, 90):
        send(f"S{a}")
        time.sleep(0.6)

    send("L1")
    print("Done.")
    ser.close()


if __name__ == "__main__":
    main()
