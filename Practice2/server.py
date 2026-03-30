#!/usr/bin/env python3
"""
TCP chat server — one client at a time.
Run first, then run client.py in another terminal.
"""

import argparse
import socket
import sys
import threading


def recv_loop(conn: socket.socket, addr: tuple, stop: threading.Event) -> None:
    try:
        while not stop.is_set():
            data = conn.recv(4096)
            if not data:
                print("\n[Client disconnected]")
                break
            text = data.decode("utf-8", errors="replace").rstrip("\n\r")
            print(f"\n<{addr[0]}:{addr[1]}> {text}")
    except OSError:
        pass
    finally:
        stop.set()


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP message server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5001, help="Port (default 5001)")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind((args.host, args.port))
        sock.listen(1)
        print(f"Listening on {args.host}:{args.port} — run client.py in another terminal.")
        print("Waiting for connection...\n")

        conn, addr = sock.accept()
        print(f"Connected: {addr[0]}:{addr[1]}\n")
        print("Type messages and press Enter to send. Ctrl+C or 'quit' to exit.\n")

        stop = threading.Event()
        t = threading.Thread(target=recv_loop, args=(conn, addr, stop), daemon=True)
        t.start()

        try:
            while not stop.is_set():
                line = sys.stdin.readline()
                if not line:
                    break
                msg = line.rstrip("\n\r")
                if msg.lower() == "quit":
                    break
                if msg:
                    conn.sendall((msg + "\n").encode("utf-8"))
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            stop.set()
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conn.close()
    finally:
        sock.close()


if __name__ == "__main__":
    main()
