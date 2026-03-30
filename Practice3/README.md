# Practice 3 — Lab Streaming Layer (LSL): outlet and inlet

### Goal

Use the **Lab Streaming Layer (LSL)** to **publish** a multi-channel stream from one process and **subscribe** to it from another. LSL is widely used in neuroscience and robotics for time-synchronized streaming over the local network.

### Concepts

- **`StreamInfo`** — describes the stream (name, type, channel count, nominal rate, format).
- **`StreamOutlet`** — pushes samples (e.g. `push_sample`) so other apps can discover and read them.
- **`resolve_byprop`** — finds streams on the network (by name, type, etc.).
- **`StreamInlet`** — pulls samples with `pull_sample` or `pull_chunk`.

### Setup

```bash
cd Practice3
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

If `pylsl` fails to load the native `liblsl` library, install the [Lab Streaming Layer](https://github.com/sccn/liblsl) for your OS or use a Python environment that ships compatible wheels (see `pylsl` documentation).

### How to run

**Terminal 1 — outlet (publisher):**

```bash
cd Practice3
python3 stream_outlet.py
```

Optional: `python3 stream_outlet.py --duration 30` to stop after 30 seconds.

**Terminal 2 — inlet (subscriber):**

```bash
cd Practice3
python3 stream_inlet.py
```

The inlet waits for a stream named `Practice3Demo` (same as the outlet). Use `python3 stream_inlet.py --max-samples 500` to print 500 samples and exit.

### Files

| File | Role |
|------|------|
| `stream_outlet.py` | Creates an LSL stream and pushes synthetic multi-channel data |
| `stream_inlet.py` | Resolves the stream by name and prints incoming samples |
| `requirements.txt` | `pylsl` |

### Notes

- Both processes can run on the **same machine**; LSL uses the local network stack.
- Stream **metadata** (name, rate, channels) must match what you resolve in the inlet.
- For real hardware, you would replace the synthetic `push_sample` loop with sensor reads at the correct rate.
