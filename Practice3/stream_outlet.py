#!/usr/bin/env python3
"""
Lab Streaming Layer (LSL) — publish a synthetic multi-channel stream.

Run this first, then run stream_inlet.py in another terminal.
Requires liblsl (installed with pylsl wheels on most platforms).
"""

import argparse
import math
import random
import time

try:
    import pylsl
except ImportError:
    raise SystemExit("Install pylsl: pip install -r requirements.txt") from None

STREAM_NAME = "Practice3Demo"
CHANNEL_COUNT = 4
NOMINAL_SRATE = 100.0


def main() -> None:
    parser = argparse.ArgumentParser(description="LSL stream outlet (synthetic data)")
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Stop after N seconds (0 = run until Ctrl+C)",
    )
    args = parser.parse_args()

    info = pylsl.StreamInfo(
        name=STREAM_NAME,
        type="EEG",
        channel_count=CHANNEL_COUNT,
        nominal_srate=NOMINAL_SRATE,
        channel_format=pylsl.cf_float32,
        source_id="practice3_outlet",
    )
    chns = info.desc().append_child("channels")
    for i in range(CHANNEL_COUNT):
        ch = chns.append_child("channel")
        ch.append_child_value("label", f"CH{i+1}")
        ch.append_child_value("unit", "microvolts")

    outlet = pylsl.StreamOutlet(info)
    print(
        f"Streaming '{STREAM_NAME}': {CHANNEL_COUNT} ch @ {NOMINAL_SRATE} Hz — "
        "run stream_inlet.py in another terminal. Ctrl+C to stop."
    )

    t0 = time.time()
    sample_index = 0
    dt = 1.0 / NOMINAL_SRATE

    try:
        while True:
            t = sample_index / NOMINAL_SRATE
            sample = [
                math.sin(2 * math.pi * 10 * t + i * 0.5) * 50.0 + random.gauss(0.0, 2.0)
                for i in range(CHANNEL_COUNT)
            ]
            outlet.push_sample(sample)
            sample_index += 1

            next_tick = t0 + sample_index * dt
            sleep_for = next_tick - time.time()
            if sleep_for > 0:
                time.sleep(sleep_for)

            if args.duration > 0 and (time.time() - t0) >= args.duration:
                break
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        del outlet


if __name__ == "__main__":
    main()
