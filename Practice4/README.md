# Practice 4 — GUI + COM port (`servoid,position`)

### Goal

A small **desktop GUI** (Tkinter) that opens a **serial (COM) port** and sends commands as:

```text
servoid,position
```

Each command is sent as one **ASCII line** ending with **newline** (e.g. `1,90` moves servo **1** to **90°**).

### Python setup

```bash
cd Practice4
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 gui_serial.py
```

### Using the app

1. Click **Refresh** if your board is not listed.
2. Choose **Port** and **Baud** (default **9600** to match the sample sketch).
3. **Connect**.
4. Enter **Servo ID** and **Position** (0–180), then **Send**.

The log shows each line sent.

### Protocol

| Field | Meaning |
|--------|--------|
| `servoid` | Integer, which servo (sample firmware: **1–4**) |
| `position` | Integer angle **0–180** |

Example: ID `2`, position `45` → bytes sent: `2,45\n`

### Arduino (optional)

Upload `arduino/servo_serial/servo_serial.ino`. It maps servo **1–4** to pins **D9–D12**. Adjust `PINS[]` if your wiring differs.

### Dependencies

- **pyserial** — see `requirements.txt`
- **Tkinter** — included with most Python installs (on Linux you may need `python3-tk`).
