from copy import deepcopy

def calculate(s: dict, effect_total: int = 0) -> dict:
    out = deepcopy(s)

    ranks = s.get("ranks", 0)
    is_class = s.get("class", False)
    has_ranks = ranks > 0

    class_bonus = 3 if has_ranks and is_class else 0

    modifier = ranks + class_bonus + effect_total

    out["modifier"] = modifier
    return out
