from rerole_lib import ability
from rerole_lib import effect

def test_ability_modifier_calculation():
    scores = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 35
    ]
    modifiers = [
        -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 7, 12
    ]

    for i, s in enumerate(scores):
        assert ability.modifier(s) == modifiers[i]

def test_complex_calculation():
    strength = {
        "score": 15,
        "damage": 3,
        "drain": 1
    }
    belt_of_strength = {
        "value": 3,
        "type": effect.type.ENHANCEMENT
    }

    # Ability drain should effectively reduce the strength score by 1; with the +3 from 
    # the belt, the effective strength modifier should be +3.
    #
    # Ability _damage_ does not change the calculation of the ability modifier 
    # directly; rather, for every 2 points of damage, anything utilizing that ability 
    # score suffers a penalty of -1
    #
    # Ergo:
    effects_should_be = [
        {
            "value": 3
        },
        {
            "value": -1
        }
    ]
    effects_are = ability.to_effects(
        ability=strength,
        effects=[belt_of_strength]
    )

    assert effects_should_be == effects_are
