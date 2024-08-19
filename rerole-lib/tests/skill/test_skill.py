from rerole_lib import character as c, skill, utils

def test_skill_calculation():
    """
    Skill calculation only has one distinct rule:

    * If a skill is a class skill and there is at least one rank in the skill, the modifier receives a +3 bonus.

    That's pretty much it. Everything else is a simple sum.
    """

    effect_total = 10

    acrobatics = {
        "ranks": 0,
        "class": True,
    }
    calc_acrobatics = skill.calculate(acrobatics, effect_total)
    assert calc_acrobatics.get("modifier") == 10

    climb = {
        "ranks": 2,
        "class": True,
    }
    skill.calculate(climb, effect_total)
    calc_climb = skill.calculate(climb, effect_total)
    assert calc_climb.get("modifier") == 15

    swim = {
        "ranks": 2,
        "class": False,
    }
    skill.calculate(swim, effect_total)
    calc_swim = skill.calculate(swim, effect_total)
    assert calc_swim.get("modifier") == 12

    sleight_of_hand = {
        "ranks": 0,
        "class": False,
    }
    skill.calculate(sleight_of_hand, effect_total)
    calc_sleight_of_hand = skill.calculate(sleight_of_hand, effect_total)
    assert calc_sleight_of_hand.get("modifier") == 10
