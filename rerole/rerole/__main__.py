import argparse
import json
import sys

from rerole_lib import character as c, utils

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        type=str,
        help="Path to character data file.",
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
