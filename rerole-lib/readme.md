# rerole-lib

This directory contains the library code used throughout the pf-rerole project.

In general, this library is written in a functional style. It is intended that state be managed by library consumers in whatever way they see fit.

## Usage

For sample data, peruse the .json files in any of the test directories.

```
import json

from rerole_lib import character

with open("tests/character/test_data.json") as f:
    data = json.load()

print(data["skills"]["climb"])
"""
{'ranks': 2, 'class': True, 'ability': 'strength'}
"""

calculated = character.calculate(data)

print(calculated["skills"]["climb"])
"""
{'ranks': 2, 'class': True, 'ability': 'strength', 'modifier': 11}
"""
```

## Development setup

Create and/or activate virtual environment:

```
$ python -m venv .venv
$ source .venv/bin/activate
```

Setup via poetry:

```
$ poetry install
```

## Testing

Via make:

```
$ make test
```

Via poetry:

```
$ poetry run pytest
```
