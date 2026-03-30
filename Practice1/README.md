# Practice 1 — pyserial + Arduino (LED + servo)

## English

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

```bash
cd "Practice 1"
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
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

## Español

### Qué es esto

Un enlace **serie** mínimo entre **Python** ([pyserial](https://pyserial.readthedocs.io/es/latest/)) y un **Arduino**: encender/apagar el **LED integrado** y mover un **servomotor** (0–180°).

### Hardware

- Arduino Uno (o compatible)
- Cable USB
- Servo: señal → **D9** (cambia `SERVO_PIN` en el sketch si hace falta), **VCC** → **5V**, **GND** → **GND**  
  *Nota: si el servo consume mucha corriente, usa fuente externa 5V y **GND común** con el Arduino.*

### Arduino

1. Abre `arduino/serial_led_servo/serial_led_servo.ino` en el Arduino IDE.
2. Elige placa y puerto, sube el programa.

**Protocolo serie** (9600 baudios, cada comando termina en salto de línea `\n`):

| Comando | Acción |
|--------|--------|
| `L1` | LED encendido |
| `L0` | LED apagado |
| `S0` … `S180` | Ángulo del servo (limitado 0–180) |

El sketch responde con líneas cortas (`OK LED`, `OK SERVO`) para depurar.

### Python

```bash
cd "Practice 1"
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd python
python control.py
```

Si hace falta, indica el puerto:

```bash
python control.py /dev/cu.usbmodem1101
python control.py COM3
```

**Puerto:** en macOS/Linux suele ser `cu.usbmodem*` o `ttyUSB0`; en Windows, `COMx` en el Administrador de dispositivos.

### Rol de pyserial

- `serial.Serial(puerto, baudios)` abre el puerto.
- `write(b"...\n")` envía bytes; el Arduino lee líneas.
- Tras abrir el puerto, muchas placas se **reinician**; un `sleep` breve deja terminar el `setup()`.

---

## Files / Archivos

| Path | Description |
|------|-------------|
| `requirements.txt` | Python dependency: `pyserial` |
| `arduino/serial_led_servo/serial_led_servo.ino` | Firmware |
| `python/control.py` | Demo: blink LED + sweep servo |
