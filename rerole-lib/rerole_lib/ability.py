import math
from rerole_lib import bonus

def to_bonuses(ability, bonuses):
    base_value = ability['value']
    drain = ability.get('drain', 0)

    modified_value = base_value + bonus.total(bonuses) - drain

    ability_bonus = {
        "value": modifier(modified_value)
    }

    out = [ability_bonus]

    ability_penalty = penalty(ability)
    if ability_penalty:
        out.append(ability_penalty)

    return out

def modifier(value):
    calculated = (value * 0.5) - 5

    return int(math.floor(calculated))

def penalty(ability):
    d = ability.get('damage')
    if not d:
        return None

    calculation = 0.5 * d
    value = -int(math.floor(calculation))

    return {
        "value": value
    }
