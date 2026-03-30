# Practice 1 — pyserial + Arduino (LED + servo)

### What this is

A minimal **serial** link between **Python** ([pyserial](https://pyserial.readthedocs.io/)) and an **Arduino**: turn the **built-in LED** on/off and set a **servo** angle (0–180°).

### Hardware

- Arduino Uno (or compatible)
- USB cable
- Servo: signal → **D9** (edit `SERVO_PIN` in the sketch if needed), **VCC** → **5V**, **GND** → **GND**  
  *Note: if the servo draws a lot of current, use an external 5V supply and common GND with the Arduino.*

### Arduino

1. Open `arduino/serial_led_servo/serial_led_servo.ino` in the Arduino IDE.
2. Select board and port, upload.

**Serial protocol** (9600 baud, each command ends with newline `\n`):

| Command | Action |
|--------|--------|
| `L1` | LED on |
| `L0` | LED off |
| `S0` … `S180` | Servo angle (clamped 0–180) |

The sketch replies with short lines like `OK LED` / `OK SERVO` for debugging.

### Python

With a virtual environment (see the workshop root `README.md`):

```bash
cd Practice1
pip install -r requirements.txt
cd python
python control.py
```

Pass the port explicitly if needed:

```bash
python control.py /dev/cu.usbmodem1101    # macOS example
python control.py COM3                    # Windows
```

**Finding the port:** macOS/Linux often show `cu.usbmodem*` or `ttyUSB0`; Windows uses `COMx` in Device Manager.

### How pyserial fits in

- `serial.Serial(port, baudrate)` opens the port (like a terminal).
- `write(b"...\n")` sends bytes; the Arduino reads lines.
- After opening, many boards **reset**; a short `sleep` lets `setup()` finish.

---

## Files

| Path | Description |
|------|-------------|
| `requirements.txt` | Python dependency: `pyserial` |
| `arduino/serial_led_servo/serial_led_servo.ino` | Firmware |
| `python/control.py` | Demo: blink LED + sweep servo |
