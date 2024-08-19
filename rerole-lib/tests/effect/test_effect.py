from rerole_lib import effect

def test_effect_stacking_rules():
    strength = {
        "value": 4
    }
    sword_enhancement = {
        "value": 1,
        "type": effect.type.ENHANCEMENT
    }
    spell = {
        "value": 3,
        "type": effect.type.ENHANCEMENT
    }
    feat_one = {
        "value": 1,
        "type": effect.type.CIRCUMSTANCE
    }
    feat_two = {
        "value": 2,
        "type": effect.type.CIRCUMSTANCE
    }
    all_bonuses = [strength, sword_enhancement, spell, feat_one, feat_two]

    str_damage = {
        "value": -2
    }
    poison = {
        "value": -3,
        "type": effect.type.ALCHEMICAL
    }
    alcohol = {
        "value": -1,
        "type": effect.type.ALCHEMICAL
    }
    all_penalties = [str_damage, poison, alcohol]

    all_effects = all_bonuses + all_penalties

    total_should_be = 5

    total_is = effect.total(all_effects)

    assert total_is == total_should_be

def test_effect_state_application():
    effects = [
        {
            "value": 1,
            "state": "active",
        },
        {
            "value": 2,
            "state": "inactive",
        },
        {
            "value": 4,
            "state": "suppressed",
        },
        {
            "value": 8,
            "state": "disabled",
        },
        {
            "type": "enhancement",
            "value": 20,
        },
    ]

    applied_should_be = [
        {
            "value": 1,
            "state": "active",
        },
        {
            "type": "enhancement",
            "value": 20,
        },
    ]
    applied_is = effect.applied(effects)
    assert applied_should_be == applied_is
