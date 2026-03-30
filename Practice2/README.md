# Practice 2 — TCP sockets (client and server)

### Goal

Learn the basics of **TCP sockets** in Python: a **server** waits for a connection; a **client** connects. Both can **send** and **receive** text from the **terminal** at the same time (using a thread for incoming messages).

### Concepts

- **`socket.socket(AF_INET, SOCK_STREAM)`** — IPv4 TCP socket.
- **Server:** `bind()` → `listen()` → `accept()` → use the returned connection socket for `recv()` / `sendall()`.
- **Client:** `connect()` → same `recv()` / `sendall()` on that socket.
- **Thread:** while you type in the main thread, another thread prints what arrives from the network.

### How to run

**Terminal 1 (server):**

```bash
cd Practice2
python3 server.py
```

Optional: `python3 server.py --host 127.0.0.1 --port 5001`

**Terminal 2 (client):**

```bash
cd Practice2
python3 client.py
```

The client defaults to `127.0.0.1:5001`. If you change the port, use the same value on both sides:

`python3 client.py --host 127.0.0.1 --port 5001`

Type a line and press **Enter** to send. Type **`quit`** or **Ctrl+C** to exit.

### Dependencies

See `requirements.txt` — this practice uses only the **standard library** (no `pip install` required).

### Same machine vs. LAN

- **Same machine:** `127.0.0.1` works.
- **LAN:** run the server with `--host 0.0.0.0`, note the server’s LAN IP, then run `python3 client.py --host <SERVER_IP>` from the other computer (you may need to allow the port in the firewall).

---

## Files

| File | Role |
|------|------|
| `server.py` | Listens, accepts one client, terminal chat |
| `client.py` | Connects to the server, terminal chat |
| `requirements.txt` | Note: no third-party packages |
