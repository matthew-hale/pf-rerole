from enum import Enum

def total(effects: list[dict]) -> int:
    """Calculate the total value of the provided effects."""
    applied_effects = applied(effects)
    if not applied_effects:
        return 0

    values = [b['value'] for b in applied_effects]

    return sum(values)

def applied(effects: list[dict]) -> list[dict]:
    """Filter out effects that do not apply due to stacking rules.

    Bonus stacking rules are not that complicated:

    * Bonuses/penalties of the same type generally do not stack, with some exceptions
    * The largest absolute value of each type of bonus and penalty will be applied
    """
    if not effects:
        return []

    penalties = list(filter(penalty, effects))
    bonuses = list(filter(bonus, effects))

    non_stacking_penalties = list(filter(non_stacking, penalties))
    non_stacking_bonuses = list(filter(non_stacking, bonuses))

    non_stacking_penalties_by_type = {}
    for p in non_stacking_penalties:
        t = p.get('type', type.UNTYPED)
        if t not in non_stacking_penalties_by_type.keys():
            non_stacking_penalties_by_type[t] = []
        non_stacking_penalties_by_type[t].append(p)

    largest_non_stacking_penalties = []
    # Sorting penalties by 'value' gives us the most negative value first
    for _, Ps in non_stacking_penalties_by_type.items():
        Ps_by_size = sorted(Ps, key=lambda p: p['value'])
        largest_P = Ps_by_size[0]
        largest_non_stacking_penalties.append(largest_P)

    non_stacking_bonuses_by_type = {}
    for b in non_stacking_bonuses:
        t = b.get('type', type.UNTYPED)
        if t not in non_stacking_bonuses_by_type.keys():
            non_stacking_bonuses_by_type[t] = []
        non_stacking_bonuses_by_type[t].append(b)

    largest_non_stacking_bonuses = []
    # Sorting bonuses by 'value' _descending_ gives us the largest value first
    for _, Bs in non_stacking_bonuses_by_type.items():
        Bs_by_size = sorted(Bs, key=lambda b: b['value'], reverse=True)
        largest_B = Bs_by_size[0]
        largest_non_stacking_bonuses.append(largest_B)

    stacking_penalties = list(filter(stacking, penalties))
    stacking_bonuses = list(filter(stacking, bonuses))

    return stacking_penalties + stacking_bonuses + largest_non_stacking_penalties + largest_non_stacking_bonuses

class type(Enum):
    UNTYPED = "untyped"
    ALCHEMICAL = "alchemical"
    ARMOR = "armor"
    BAB = "bab"
    CIRCUMSTANCE = "circumstance"
    COMPETENCE = "competence"
    DEFLECTION = "deflection"
    DODGE = "dodge"
    ENHANCEMENT = "enhancement"
    INHERENT = "inherent"
    INSIGHT = "insight"
    LUCK = "luck"
    MORALE = "morale"
    NATURAL_ARMOR = "natural armor"
    PROFANE = "profane"
    RACIAL = "racial"
    RESISTANCE = "resistance"
    SACRED = "sacred"
    SHIELD = "shield"
    SIZE = "size"
    TRAIT = "trait"


_stacking = [type.CIRCUMSTANCE, type.DODGE, type.UNTYPED, None]

def stacking(e: dict) -> bool:
    t = e.get("type")
    return t in _stacking

def non_stacking(e: dict) -> bool:
    return not stacking(e)

def penalty(e: dict) -> bool:
    return e["value"] < 0

def bonus(e: dict) -> bool:
    return not penalty(e)
