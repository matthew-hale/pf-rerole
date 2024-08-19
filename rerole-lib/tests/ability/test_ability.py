from rerole_lib import ability

def test_ability_modifier_calculation():
    scores = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 35
    ]
    modifiers = [
        -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 7, 12
    ]

    for i, s in enumerate(scores):
        assert ability.modifier(s) == modifiers[i]

def test_calculate():
    strength = {
        "score": 15,
        "damage": 3,
        "drain": 1
    }
    effect_total = 4
    calc_strength = ability.calculate(strength, effect_total)

    assert calc_strength.get("modifier") == 4
    assert ability.penalty(calc_strength) == {
        "value": -1
    }
