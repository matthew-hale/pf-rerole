import math
from rerole_lib import effect

def to_effects(ability: dict, effects: list[dict]) -> list[dict]:
    base_value = ability['score']
    drain = ability.get('drain', 0)

    modified_value = base_value + effect.total(effects) - drain

    ability_bonus = {
        "value": modifier(modified_value)
    }

    out = [ability_bonus]

    ability_penalty = penalty(ability)
    if ability_penalty:
        out.append(ability_penalty)

    return out

def modifier(score: int) -> int:
    """Calculates the appropriate ability modifier given an integer input representing an ability score."""
    calculated = (score * 0.5) - 5

    return int(math.floor(calculated))

def penalty(ability: dict) -> dict:
    d = ability.get('damage')
    if not d:
        return None

    calculation = 0.5 * d
    value = -int(math.floor(calculation))

    return {
        "value": value
    }
