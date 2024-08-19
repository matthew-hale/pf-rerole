import json
import sys

from rerole_lib import character as c, utils

from .lib import usage

def main():
    args = sys.argv[1:]
    if not args or args[0] == "-h":
        print(usage)
        sys.exit(0)

    filepath = args[0]
    with open(filepath) as f:
        data = c.load(f)
    print(json.dumps(c.calculate(data), indent=4))

if __name__ == "__main__":
    main()
