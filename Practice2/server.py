#!/usr/bin/env python3
"""
TCP chat server — multiple clients.

Start this server, then run `client.py` in multiple terminals.
By default, it broadcasts any received client message to all connected clients.
"""

import argparse
import socket
import sys
import threading


def client_recv_loop(
    conn: socket.socket,
    addr: tuple,
    stop: threading.Event,
    clients: dict[socket.socket, tuple[str, int]],
    clients_lock: threading.Lock,
) -> None:
    """
    Receive lines from a single client and broadcast them to others.
    Protocol: client sends UTF-8 lines terminated by '\n'.
    """
    buffer = b""
    try:
        while not stop.is_set():
            data = conn.recv(4096)
            if not data:
                break

            buffer += data
            while b"\n" in buffer:
                line_bytes, buffer = buffer.split(b"\n", 1)
                line_bytes = line_bytes.rstrip(b"\r")
                if not line_bytes:
                    continue

                text = line_bytes.decode("utf-8", errors="replace")
                if text.lower() == "quit":
                    # Disconnect only this client.
                    return

                prefix = f"{addr[0]}:{addr[1]}"
                print(f"\n<{prefix}> {text}")
                broadcast(f"<{prefix}> {text}", clients, clients_lock)
    except OSError:
        # Socket closed / connection reset.
        pass
    finally:
        with clients_lock:
            clients.pop(conn, None)
        try:
            conn.close()
        except OSError:
            pass


def broadcast(message: str, clients: dict[socket.socket, tuple[str, int]], clients_lock: threading.Lock) -> None:
    """Send message to all connected clients (best-effort)."""
    dead: list[socket.socket] = []
    payload = (message + "\n").encode("utf-8")
    with clients_lock:
        targets = list(clients.keys())

    for c in targets:
        try:
            c.sendall(payload)
        except OSError:
            dead.append(c)

    if dead:
        with clients_lock:
            for c in dead:
                clients.pop(c, None)


def operator_loop(
    stop: threading.Event,
    clients: dict[socket.socket, tuple[str, int]],
    clients_lock: threading.Lock,
) -> None:
    """Read server operator input from stdin and broadcast it."""
    try:
        while not stop.is_set():
            line = sys.stdin.readline()
            if not line:
                break
            msg = line.rstrip("\n\r")
            if msg.lower() in {"quit", "shutdown"}:
                stop.set()
                break
            if msg:
                broadcast(f"[server] {msg}", clients, clients_lock)
    except KeyboardInterrupt:
        stop.set()


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP message server")
    parser.add_argument("--host", default="192.168.0.17", help="Bind address (default 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5001, help="Port (default 5001)")
    args = parser.parse_args()

    stop = threading.Event()
    clients: dict[socket.socket, tuple[str, int]] = {}
    clients_lock = threading.Lock()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(1.0)  # allow periodic stop checks

    try:
        sock.bind((args.host, args.port))
        sock.listen(10)
        print(f"Listening on {args.host}:{args.port}")
        print("Run client.py in other terminals. Type messages here to broadcast.")
        print("Server operator: Ctrl+C or 'quit' to stop.\n")

        op_thread = threading.Thread(
            target=operator_loop,
            args=(stop, clients, clients_lock),
            daemon=True,
        )
        op_thread.start()

        while not stop.is_set():
            try:
                conn, addr = sock.accept()
            except TimeoutError:
                continue

            with clients_lock:
                clients[conn] = (addr[0], addr[1])
            print(f"Connected: {addr[0]}:{addr[1]}")

            t = threading.Thread(
                target=client_recv_loop,
                args=(conn, addr, stop, clients, clients_lock),
                daemon=True,
            )
            t.start()
    finally:
        stop.set()

        with clients_lock:
            for c in list(clients.keys()):
                try:
                    c.close()
                except OSError:
                    pass

        try:
            sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
