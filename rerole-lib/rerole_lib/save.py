from copy import deepcopy

def calculate(s: dict, effect_total: int) -> dict:
    s = deepcopy(s)

    modifier = s.get("value", 0) + effect_total
    s["modifier"] = modifier

    return s
