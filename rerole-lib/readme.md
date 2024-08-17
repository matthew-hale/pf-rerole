# rerole-lib

This directory contains the library code used throughout the pf-rerole project.

In general, this library is written in a functional style. It is intended that state be managed by library consumers in whatever way they see fit.

## Usage

For sample data, peruse the .json files in any of the test directories.

Here's how one would calculate the modifier of a character's "acrobatics" skill:

```
from rerole_lib import character

data = character.load("path/to/data.json")
effect_index = character.build_effect_index(data)

character.roll_skill(data, effect_index, "acrobatics")

"""
Result should be:
    skill ranks
  + class skill bonus (if applicable)
  + associated ability modifier (dynamically calculated)
  + effects applying to skill
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
