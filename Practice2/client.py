#!/usr/bin/env python3
"""
TCP chat client — connects to server.py.
Run server.py first, then this script.
"""

import argparse
import socket
import sys
import threading


def recv_loop(sock: socket.socket, stop: threading.Event) -> None:
    try:
        while not stop.is_set():
            data = sock.recv(4096)
            if not data:
                print("\n[Server closed the connection]")
                break
            text = data.decode("utf-8", errors="replace").rstrip("\n\r")
            print(f"\n<server> {text}")
    except OSError:
        pass
    finally:
        stop.set()


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP client")
    parser.add_argument("--host", default="127.0.0.1", help="Server IP address")
    parser.add_argument("--port", type=int, default=5001, help="Port (default 5001)")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((args.host, args.port))
        print(f"Connected to {args.host}:{args.port}")
        print("Type messages and press Enter to send. Ctrl+C or 'quit' to exit.\n")

        stop = threading.Event()
        t = threading.Thread(target=recv_loop, args=(sock, stop), daemon=True)
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
                    sock.sendall((msg + "\n").encode("utf-8"))
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            stop.set()
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
    except ConnectionRefusedError:
        print(f"Could not connect to {args.host}:{args.port}. Is server.py running?")
        sys.exit(1)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
