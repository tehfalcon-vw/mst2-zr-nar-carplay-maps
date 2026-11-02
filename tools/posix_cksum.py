#!/usr/bin/env python3
"""Print the POSIX cksum CRC and byte count for one or more files."""

from pathlib import Path
import sys


def posix_cksum(data: bytes) -> int:
    crc = 0
    for value in data:
        crc ^= value << 24
        for _ in range(8):
            crc = (((crc << 1) ^ 0x04C11DB7) if crc & 0x80000000 else crc << 1) & 0xFFFFFFFF
    length = len(data)
    while length:
        crc ^= (length & 0xFF) << 24
        length >>= 8
        for _ in range(8):
            crc = (((crc << 1) ^ 0x04C11DB7) if crc & 0x80000000 else crc << 1) & 0xFFFFFFFF
    return (~crc) & 0xFFFFFFFF


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {Path(sys.argv[0]).name} FILE [...]", file=sys.stderr)
        return 2
    for name in sys.argv[1:]:
        path = Path(name)
        data = path.read_bytes()
        print(posix_cksum(data), len(data), path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
