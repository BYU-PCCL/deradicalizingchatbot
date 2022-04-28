# VS Code doesn't correctly re-encode all characters, including emoji. This script does.
# To correctly re-encode CSVs created from Chris Bail's files:
# python3 reencode.py utf8 macroman <file(s)>

from pathlib import Path


def reencode_file(filename, decode_encoding, encode_encoding):
    filename = Path(filename)
    with open(filename, "r", encoding=decode_encoding) as f:
        content = f.read()
    encoded_filename = filename.with_name(
        filename.stem + ".reencoded" + "".join(filename.suffixes)
    )
    with open(encoded_filename, "w", encoding=encode_encoding) as f:
        f.write(content)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Re-encode file(s).")
    parser.add_argument("decode", help="Decode file(s) using this encoding.")
    parser.add_argument("encode", help="Encode file(s) using this encoding.")
    parser.add_argument("files", nargs="+", help="Files to re-encode.")
    args = parser.parse_args()

    for filename in args.files:
        if ".reencoded" in filename:
            continue
        reencode_file(filename, args.decode, args.encode)
