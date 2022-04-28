#!/usr/bin/env python3

# VS Code doesn't correctly re-encode all characters, including emoji. This script does.
# To correctly re-encode Chris Bail's files:
# reencode.py --in-place utf8 macroman <file(s)>

import logging
from functools import partial
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def _pandas_reencode_row(row, from_encoding, to_encoding):
    keys = row.keys()
    for key in keys:
        if isinstance(row[key], str):
            row[key] = row[key].encode(to_encoding).decode(from_encoding)
    return row


def _reencode_xlsx(read_path, write_path, from_encoding, to_encoding):
    """Re-encode an XLSX file"""
    logger.warning(
        f"Re-encoding Excel file '{read_path.name}' using pandas, will lose formatting"
        " information."
    )
    df = pd.read_excel(read_path)
    row_apply_fn = partial(
        _pandas_reencode_row,
        from_encoding=from_encoding,
        to_encoding=to_encoding,
    )
    df.apply(row_apply_fn, axis=1).to_excel(write_path, index=False)


def _reencode_plaintext(read_path, write_path, from_encoding, to_encoding):
    """Re-encode a plaintext file"""
    with open(read_path, "r", encoding=from_encoding) as f:
        content = f.read()
    with open(write_path, "w", encoding=to_encoding) as f:
        f.write(content)


def reencode_file(filename, from_encoding, to_encoding, *, in_place=False):
    filename = Path(filename)
    if in_place:
        encoded_filename = filename
    else:
        encoded_filename = filename.with_name(
            filename.stem + ".reencoded" + "".join(filename.suffixes)
        )

    if filename.suffix == ".xlsx":
        _reencode_xlsx(filename, encoded_filename, from_encoding, to_encoding)
        return

    _reencode_plaintext(filename, encoded_filename, from_encoding, to_encoding)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Re-encode file(s).")
    parser.add_argument("from_encoding", help="Decode file(s) using this encoding.")
    parser.add_argument("to_encoding", help="Encode file(s) using this encoding.")
    parser.add_argument("files", nargs="+", help="Files to re-encode.")
    parser.add_argument("--in-place", action="store_true", help="Re-encode in place.")

    args = parser.parse_args()

    for filename in args.files:
        if ".reencoded" in filename:
            continue
        reencode_file(
            filename, args.from_encoding, args.to_encoding, in_place=args.in_place
        )
