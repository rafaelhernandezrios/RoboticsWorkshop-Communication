#!/usr/bin/env python3
"""
Lab Streaming Layer (LSL) — resolve and subscribe to a stream by name.

Run stream_outlet.py first so a stream is available on the network.
"""

import argparse
import sys
import time

try:
    import pylsl
except ImportError:
    raise SystemExit("Install pylsl: pip install -r requirements.txt") from None

STREAM_NAME = "Practice3Demo"
DEFAULT_TIMEOUT = 10.0


def main() -> None:
    parser = argparse.ArgumentParser(description="LSL stream inlet (receive samples)")
    parser.add_argument(
        "--name",
        default=STREAM_NAME,
        help="Stream name to resolve (must match the outlet)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Seconds to wait for the stream to appear",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=0,
        help="Stop after N samples (0 = run until Ctrl+C)",
    )
    args = parser.parse_args()

    print(f"Looking for stream named '{args.name}' (timeout {args.timeout}s)...")
    streams = pylsl.resolve_byprop("name", args.name, timeout=args.timeout)
    if not streams:
        print(
            f"No stream named '{args.name}' found. Start stream_outlet.py first.",
            file=sys.stderr,
        )
        sys.exit(1)

    inlet = pylsl.StreamInlet(streams[0])
    info = inlet.info()
    print(
        f"Connected: {info.name()} | {info.channel_count()} ch @ "
        f"{info.nominal_srate()} Hz | type={info.type()}"
    )
    print("Receiving... Ctrl+C to stop.\n")

    count = 0
    t0 = time.time()
    try:
        while True:
            sample, ts = inlet.pull_sample(timeout=2.0)
            if sample is None:
                continue
            count += 1
            ch_str = ", ".join(f"{v:8.3f}" for v in sample)
            print(f"sample {count:6d}  t={ts:12.6f}  [{ch_str}]")

            if args.max_samples > 0 and count >= args.max_samples:
                break
    except KeyboardInterrupt:
        elapsed = time.time() - t0
        rate = count / elapsed if elapsed > 0 else 0
        print(f"\nStopped. Received {count} samples (~{rate:.1f} samples/s).")


if __name__ == "__main__":
    main()
