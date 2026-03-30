# Practice 5 — TCP bridge + GUI sliders (`servoid,position`)

### Goal

- **Server:** Listens for a **TCP** client, receives lines `servoid,position`, and **forwards them to a serial (COM) port** (same format as Practice 4).
- **Client:** Connects over TCP and drives **four sliders** (servos **1–4**) in near real time; sends are **debounced** (~45 ms) to avoid flooding the serial link.

### Setup

```bash
cd Practice5
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### How to run

1. Flash an Arduino sketch that understands `servoid,position` lines (e.g. `Practice4/arduino/servo_serial/servo_serial.ino` — servos 1–4 on D9–D12, 9600 baud).

2. **Server** (machine with the USB cable):

   ```bash
   python3 server.py
   ```

   - **Open serial** (COM + baud **9600**).
   - **Start TCP server** (default bind `0.0.0.0`, port **5005**).

3. **Client** (same PC or another on the LAN):

   ```bash
   python3 client.py
   ```

   - Set **Host** to `127.0.0.1` (same machine) or the server’s **LAN IP**.
   - **Port** **5005** (must match the server).
   - **Connect**, then move **Sliders** — each move schedules a line like `1,90` over TCP.

### Protocol

- **TCP payload:** UTF-8 text, one command per line, newline-terminated: `servoid,position` (e.g. `2,45`).
- **Serial:** the server writes the same line (including `\n`) to the COM port.

### Files

| File | Role |
|------|------|
| `server.py` | GUI: serial + TCP listener → forward to COM |
| `client.py` | GUI: sliders → TCP to server |
| `requirements.txt` | `pyserial` |

### Notes

- **Tkinter:** on Linux, install `python3-tk` if the GUI fails to start.
- **Firewall:** allow TCP **5005** on the server if the client is on another computer.
- The server accepts **one client at a time**; after disconnect, it waits for the next.
