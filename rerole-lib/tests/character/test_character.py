from rerole_lib import character as c, utils

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

def test_calculate():
    with open("tests/character/test_data.json") as f:
        data = c.load(f)
    data = c.calculate(data)

    assert utils.get_in(data, ["skills", "climb", "modifier"]) == 11
