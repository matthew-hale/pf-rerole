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
    modifier = s.get("value", 0) + effect_total
    s["modifier"] = modifier
