# Workshop 3 — Robotics (Python, Arduino, networking)

This repository is a set of **hands-on practices**: serial communication with Arduino, TCP sockets, Lab Streaming Layer (LSL), desktop GUIs, and a TCP-to-serial bridge for servo control.

---

## Prerequisites

- **Python 3** (3.10 or newer recommended). Check with:
  - **macOS:** `python3 --version`
  - **Windows:** `py --version` or `python --version`
- **Arduino IDE** (for practices that include `.ino` sketches).
- For **Practice 4** and **Practice 5** GUIs on **Linux**, you may need the `python3-tk` package; on **macOS** and **Windows**, Tkinter is usually bundled with the official Python installer.

---

## Python virtual environment (venv)

Use a **virtual environment** so project dependencies stay isolated from your system Python.

### 1. Open a terminal in the workshop folder

- **macOS:** Terminal → `cd` to this folder (e.g. drag the folder into Terminal to paste the path).
- **Windows:** Command Prompt or PowerShell → `cd` to this folder.

### 2. Create the venv (once per project)

**macOS**

```bash
python3 -m venv .venv
```

**Windows (Command Prompt)**

```cmd
py -m venv .venv
```

If `py` is not found, try:

```cmd
python -m venv .venv
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
```

### 3. Activate the venv

You must activate the venv **every time** you open a new terminal session before running the exercises.

**macOS**

```bash
source .venv/bin/activate
```

After activation, your prompt usually shows `(.venv)`.

**Windows — Command Prompt**

```cmd
.venv\Scripts\activate.bat
```

**Windows — PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell shows an execution policy error, run once (as Administrator if needed):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### 4. Upgrade pip (optional but recommended)

```bash
python -m pip install --upgrade pip
```

### 5. Install dependencies for each practice

Each practice folder has its own `requirements.txt`. From the **workshop root** with the venv **activated**:

```bash
pip install -r Practice1/requirements.txt
```

Repeat with `Practice2/requirements.txt`, `Practice3/requirements.txt`, etc., when you need that practice.  
**Practice 2** uses only the Python standard library (no extra `pip` packages).

---

## Practices overview

| Folder | Topic |
|--------|--------|
| **Practice1** | **pyserial** + Arduino: built-in LED and servo (`L` / `S` commands). See `Practice1/README.md`. |
| **Practice2** | **TCP sockets**: terminal chat **server** and **client**. See `Practice2/README.md`. |
| **Practice3** | **LSL (Lab Streaming Layer)**: `stream_outlet.py` publishes a stream; `stream_inlet.py` subscribes. See `Practice3/README.md`. |
| **Practice4** | **Tkinter GUI** + COM port: send `servoid,position` to Arduino. See `Practice4/README.md`. |
| **Practice5** | **Tkinter server + client**: TCP bridge to serial; sliders send servo positions in real time. See `Practice5/README.md`. |

Open each practice’s **README** for exact run commands, ports, and hardware notes.

---

## Quick reference: run a script (venv activated)

```bash
cd Practice2
python server.py
```

On **Windows**, use `python` consistently if `python3` is not on your `PATH`.

---

## Deactivate the venv

When you are done:

```bash
deactivate
```

This works the same on **macOS** and **Windows** once the venv was activated.
# RoboticsWorkshop-Communication
