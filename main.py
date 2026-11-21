#!/usr/bin/env python3
"""Deliver the Solmara travel poster to the make.fun grader.

The artwork itself is entry.png, committed beside this file: a single
832x1024 vintage travel poster for Solmara, a place that does not
exist — a colossal stone arch framing the setting sun over a turquoise
bay, a terracotta-roofed village at its feet, the place's name set
into the sky in classic poster lettering. This script is the delivery
step. It proves the committed poster still satisfies the
competition's intake rules (PNG or JPEG, at most 1 MiB, at most
1024x1024), copies it byte-for-byte into the output directory, and
proves the copy by reading it back and comparing SHA-256 digests.
"""

import hashlib
import os
import struct
import sys
import zlib

PLACE = "Solmara"
TAGLINE = "Where the sun comes to rest"

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
BYTE_LIMIT = 1024 * 1024
DIM_LIMIT = 1024
OK_FORMATS = {"PNG", "JPEG"}


def digest(path):
    """SHA-256 of a file, streamed in 64 KiB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8"
# Start-of-frame markers carry the frame dimensions; C4 (DHT), C8
# (JPG) and CC (DAC) sit in the same numeric range but do not.
JPEG_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
# Markers with no length field and no payload: TEM, SOI, EOI, RST0-7.
JPEG_STANDALONE = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))


def image_info(path):
    """Return (format, width, height) read from the image header.

    Standard library only: the grader runs a bare python3 with no
    Pillow installed, so the header bytes are parsed directly.
    Raises ValueError when the file is neither PNG nor JPEG, or its
    header is truncated.
    """
    with open(path, "rb") as fh:
        head = fh.read(33)
        if head.startswith(PNG_SIGNATURE):
            # The IHDR chunk's data is always exactly 13 bytes, so the
            # length field in front of the chunk type must say so; a
            # different value means the header is not a real IHDR.
            (ihdr_size,) = struct.unpack(">I", head[8:12])
            if len(head) < 33 or ihdr_size != 13 or head[12:16] != b"IHDR":
                raise ValueError("entry.png has a truncated PNG header")
            width, height = struct.unpack(">II", head[16:24])
            (stored_crc,) = struct.unpack(">I", head[29:33])
            if (zlib.crc32(head[12:29]) & 0xFFFFFFFF) != stored_crc:
                raise ValueError(
                    "entry.png has a corrupt PNG IHDR chunk "
                    "(CRC-32 mismatch)")
            return "PNG", width, height
        if not head.startswith(JPEG_SIGNATURE):
            raise ValueError("entry.png is neither PNG nor JPEG")
        fh.seek(2)
        while True:
            byte = fh.read(1)
            if not byte:
                raise ValueError("entry.png has a truncated JPEG header")
            if byte != b"\xff":
                continue
            marker = fh.read(1)
            while marker == b"\xff":
                marker = fh.read(1)
            if not marker:
                raise ValueError("entry.png has a truncated JPEG header")
            code = marker[0]
            if code == 0x00 or code in JPEG_STANDALONE:
                continue
            raw = fh.read(2)
            if len(raw) < 2:
                raise ValueError("entry.png has a truncated JPEG header")
            (segment,) = struct.unpack(">H", raw)
            if segment < 2:
                # The length field counts its own two bytes, so a
                # smaller value is corrupt; trusting it would make
                # the seek below land inside the segment it skips.
                raise ValueError("entry.png has a corrupt JPEG header")
            if code in JPEG_SOF:
                frame = fh.read(5)
                if len(frame) < 5:
                    raise ValueError(
                        "entry.png has a truncated JPEG header")
                height, width = struct.unpack(">HH", frame[1:5])
                return "JPEG", width, height
            fh.seek(segment - 2, os.SEEK_CUR)


def check_source(path):
    """Return (format, width, height, size) for a valid entry image.

    Raises ValueError with the failed rule named when the committed
    poster does not satisfy the intake caps.
    """
    if not os.path.isfile(path):
        raise ValueError("entry.png is missing from the repository")
    size = os.path.getsize(path)
    if size > BYTE_LIMIT:
        raise ValueError("entry.png is %d bytes, over the 1 MiB cap" % size)
    fmt, width, height = image_info(path)
    if fmt not in OK_FORMATS:
        raise ValueError("entry.png is %s, not PNG or JPEG" % fmt)
    if width < 1 or height < 1:
        # A header can parse yet declare no pixels at all; such a
        # file is not a whole image and the gate would refuse it.
        raise ValueError(
            "entry.png declares %dx%d pixels, not a whole image"
            % (width, height))
    if width > DIM_LIMIT or height > DIM_LIMIT:
        raise ValueError(
            "entry.png is %dx%d, over the 1024x1024 cap" % (width, height))
    return fmt, width, height, size


def deliver(source, out_dir):
    """Copy the poster into out_dir and verify the copy byte-for-byte."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(source, "rb") as fh:
        payload = fh.read()
    with open(target, "wb") as fh:
        fh.write(payload)
    if digest(target) != digest(source):
        raise ValueError("the delivered copy does not match entry.png")
    return target


def main():
    fmt, width, height, size = check_source(SOURCE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = deliver(SOURCE, out_dir)
    print("%s — %s" % (PLACE, TAGLINE))
    print("entry.png: %s %dx%d, %d bytes" % (fmt, width, height, size))
    print("delivered to %s (sha256 %s)" % (target, digest(target)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        # A poster that fails the intake rules is a hard failure: say
        # which rule broke and exit non-zero so the run is not counted.
        print("entry refused: %s" % exc, file=sys.stderr)
        sys.exit(2)
