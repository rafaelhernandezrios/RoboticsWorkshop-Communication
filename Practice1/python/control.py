#!/usr/bin/env python3
"""
Simple example: control Arduino over serial with pyserial.

Set SERIAL_PORT for your OS:
  Windows:       COM3   (or whatever appears in Device Manager)
  macOS:         /dev/cu.usbmodem1101   (or run: ls /dev/cu.*)
  Linux:         /dev/ttyUSB0           (or: ls /dev/ttyUSB*)

Replace SERIAL_PORT below, then run:
  python control.py

Type commands such as L1, L0, S90 and press Enter to send them.
Type 'exit' to quit.
"""

import sys
import time

try:
    import serial
except ImportError:
    print("Install pyserial: pip install pyserial")
    sys.exit(1)

# SERIAL_PORT = "COM3"          # Windows
SERIAL_PORT = "/dev/tty.usbmodemF412FA6EE7842"   # macOS
# SERIAL_PORT = "/dev/ttyUSB0"           # Linux

BAUDRATE = 9600

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    except serial.SerialException as e:
        print(f"Could not open port {SERIAL_PORT}: {e}")
        sys.exit(1)

    print(f"Connected to {SERIAL_PORT} @ {BAUDRATE} baud.")
    print("Type commands like L1, L0, S90, press Enter (type 'exit' to quit)")
    time.sleep(2)  # Wait for Arduino reset after opening serial

    while True:
        try:
            cmd = input(">> ").strip()
            if cmd.lower() == "exit":
                break
            if cmd:
                ser.write((cmd + "\n").encode("ascii"))
                time.sleep(0.1)
                if ser.in_waiting:
                    print("[Arduino] " + ser.read(ser.in_waiting).decode("utf-8", errors="replace").strip())
        except KeyboardInterrupt:
            break

    ser.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
