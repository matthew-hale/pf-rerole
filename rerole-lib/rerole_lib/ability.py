import math

from copy import deepcopy

def calculate(a: dict, effect_total: int = 0):
    out = deepcopy(a)
    base_value = out.get("score", 0)
    drain = out.get("drain", 0)

    modified_score = base_value - drain + effect_total
    out["modified_score"] = modified_score
    out["modifier"] = modifier(modified_score)

    return out

def modifier(score: int) -> int:
    """Calculates the appropriate ability modifier given an integer input representing an ability score."""
    calculated = (score * 0.5) - 5

    return int(math.floor(calculated))

def penalty(ability: dict) -> int:
    d = ability.get("damage", 0)
    if d == 0:
        return 0

    calculation = 0.5 * d
    value = -int(math.floor(calculation))

    return value
