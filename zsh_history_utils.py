#!/usr/bin/env python3

"""Zsh history utils."""

import codecs
import sys
from argparse import ArgumentParser, FileType, Namespace
from collections.abc import Iterator
from contextlib import closing
from io import BytesIO
from typing import Final, Protocol

META: Final = 0x83
MARKER: Final = 0xA2
POUND: Final = 0x84
LAST_NORMAL_TOK: Final = 0x9C
SNULL: Final = 0x9D
NULARG: Final = 0xA1


def is_meta(byte: int) -> bool:
    return (
        byte in {0, META, MARKER}
        or POUND <= byte <= LAST_NORMAL_TOK
        or SNULL <= byte <= NULARG
    )


def unmetafy(source: BytesIO) -> Iterator[bytes]:
    skipped = False
    for line in source:
        buffer = bytearray()
        for byte in line:
            if byte == META:
                skipped = True
                continue
            buffer.append(byte ^ 32 if skipped else byte)
            skipped = False
        yield bytes(buffer)


def metafy(source: BytesIO) -> Iterator[bytes]:
    for line in source:
        buffer = bytearray()
        for byte in line:
            if is_meta(byte):
                buffer.append(META)
                buffer.append(byte ^ 32)
                continue
            buffer.append(byte)
        yield bytes(buffer)


class HasSource(Protocol):
    source: BytesIO


def decode(args: HasSource) -> None:
    with closing(args.source) as source:
        sys.stdout.writelines(
            codecs.iterdecode(unmetafy(source), "utf-8", errors="replace")
        )


def encode(args: HasSource) -> None:
    with closing(args.source) as source:
        sys.stdout.buffer.writelines(metafy(source))


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Zsh history utils")

    subparsers = parser.add_subparsers()

    parser_decode = subparsers.add_parser(
        "decode",
        help="Transform zsh history file to UTF-8 text.",
    )
    parser_decode.add_argument(
        "source",
        nargs="?",
        type=FileType("rb"),
        default="-",
        help="Target file (default: stdin)",
    )
    parser_decode.set_defaults(func=decode)

    parser_encode = subparsers.add_parser(
        "encode",
        help="Transform UTF-8 text to zsh history file.",
    )
    parser_encode.add_argument(
        "source",
        nargs="?",
        type=FileType("rb"),
        default="-",
        help="Target file (default: stdin)",
    )
    parser_encode.set_defaults(func=encode)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.func(args)

    return 0


if __name__ == "__main__":
    main()
