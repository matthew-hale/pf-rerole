import argparse
import json
import sys

from rerole_lib import character as c, utils

_output_formats = ["text", "json"]

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        type=str,
        help="Path to character data file.",
    )
    parser.add_argument(
        "--format", "-f",
        choices=_output_formats,
        default=_output_formats[0],
        help="Output format",
    )

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    filepath = args.filename
    with open(filepath) as f:
        data = c.load(f)
    print(json.dumps(c.calculate(data), indent=4))

if __name__ == "__main__":
    main()
