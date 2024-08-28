from copy import deepcopy

def default() -> dict:
    return {
        "fortitude": {
            "ability": "constitution",
        },
        "reflex": {
            "ability": "dexterity",
        },
        "will": {
            "ability": "wisdom",
        },
    }

def calculate(s: dict, effect_total: int):
    s = deepcopy(s)

    modifier = s.get("value", 0) + effect_total
    s["modifier"] = modifier

    return s
