import math

def default() -> dict:
    return {
        "strength": {
            "score": 10,
        },
        "dexterity": {
            "score": 10,
        },
        "constitution": {
            "score": 10,
        },
        "intelligence": {
            "score": 10,
        },
        "wisdom": {
            "score": 10,
        },
        "charisma": {
            "score": 10,
        },
    }

def calculate(a: dict, effect_total: int = 0):
    """Calculate a new ability score and modifier, and add them to the input dict."""
    base_value = a.get("score", 0)
    drain = a.get("drain", 0)

    modified_score = base_value - drain + effect_total
    a["modified_score"] = modified_score
    a["modifier"] = modifier(modified_score)

def modifier(score: int) -> int:
    """Calculates the appropriate ability modifier given an integer input representing an ability score."""
    calculated = (score * 0.5) - 5

    return int(math.floor(calculated))

def penalty(a: dict) -> int:
    damage = a.get("damage", 0)
    if damage == 0:
        return 0

    calculation = 0.5 * damage
    value = -int(math.floor(calculation))

    return value
