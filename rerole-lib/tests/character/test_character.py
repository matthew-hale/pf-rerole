from rerole_lib import character as c
from rerole_lib import utils

def test_build_effect_index():
    data = {
        "abilities": {
            "strength": {
                "score": 13,
            },
            "dexterity": {
                "score": 16,
            },
            "intelligence": {
                "score": 9,
            },
            "wisdom": {
                "score": 10,
            },
        },
        "spells": {
            "mighty strength": {
                "description": "As bull’s strength, except it grants a +8 enhancement bonus to Strength.",
                "value": 8,
                "magical": True,
                "tags": [
                    "cleric",
                    "paladin",
                ],
                "affects": {
                    "group": "abilities",
                    "name": "strength",
                },
            },
            "super cool": {
                "description": "Buff to multiple groups of things",
                "value": 1,
                "affects": {
                    "group": ["abilities", "skills"],
                }
            },
            "special deity power": {
                "description": "Gives a single buff to some specific ability scores.",
                "value": 2,
                "magical": True,
                "affects": {
                    "group": "abilities",
                    "name": ["strength", "wisdom"],
                },
            },
        },
        "equipment": {
            "belt of physical stuff": {
                "description": "Gives +4 to all physical ability scores.",
                "value": 4,
                "affects": {
                    "group": "abilities",
                    "name": ["strength", "dexterity", "constitution"],
                },
            },
            "headband of certain mental acuity": {
                "description": "+6 to Int, +4 to Wis.",
                1: {
                    "value": 6,
                    "affects": {
                        "group": "abilities",
                        "name": "intelligence",
                    },
                },
                2: {
                    "value": 4,
                    "affects": {
                        "group": "abilities",
                        "name": "wisdom",
                    },
                },
            },
        },
    }

    effect_index = c.build_effect_index(data)

    assert effect_index["strength"] == [
        ["spells", "mighty strength"],
        ["spells", "super cool"],
        ["spells", "special deity power"],
        ["equipment", "belt of physical stuff"],
    ]

    assert effect_index["dexterity"] == [
        ["spells", "super cool"],
        ["equipment", "belt of physical stuff"],
    ]

    assert effect_index["intelligence"] == [
        ["spells", "super cool"],
        ["equipment", "headband of certain mental acuity", 1],
    ]

    assert effect_index["wisdom"] == [
        ["spells", "super cool"],
        ["spells", "special deity power"],
        ["equipment", "headband of certain mental acuity", 2],
    ]

def test_correct_skill_modifier():
    data = c.load("tests/character/test_data.json")
    effect_index = c.build_effect_index(data)

    """Character data:
    Strength:
      Score: 15
      Damage: 3
      Drain: 1

    Climb:
      Ranks: 2
      Class skill: True
      Ability: Strength

    Spells:
      Mighty Strength:
        +8 Enhancement to Strength
      General Skill Buff:
        +1 to all skills
    Equipment:
      Belt of Stronk:
        +4 Enhancement to Strength (cancelled out by Mighty Strength)

    Effective Strength score: 22
      15 - 1 (drain) +8 (Mighty Strength)
    Effective Strength modifier: 6
    Strength damage penalty: -1

    Skill modifier: 11
      2 (ranks)
     +3 (class skill)
     +6 (strength mod)
     -1 (strength damage penalty)
     +1 (general skill buff spell)"""

    skill_mod = c.roll_skill(data, effect_index, "climb")
    assert skill_mod == 11
