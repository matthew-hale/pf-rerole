from rerole_lib import character as c, skill

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
    skill.calculate(acrobatics, effect_total)
    assert acrobatics.get("modifier") == 10

    climb = {
        "ranks": 2,
        "class": True,
    }
    skill.calculate(climb, effect_total)
    assert climb.get("modifier") == 15

    swim = {
        "ranks": 2,
        "class": False,
    }
    skill.calculate(swim, effect_total)
    assert swim.get("modifier") == 12

    sleight_of_hand = {
        "ranks": 0,
        "class": False,
    }
    skill.calculate(sleight_of_hand, effect_total)
    assert sleight_of_hand.get("modifier") == 10
