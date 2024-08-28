def default() -> dict:
    return {
        "acrobatics": {
            "ability": "dexterity",
        },
        "appraise": {
            "ability": "intelligence",
        },
        "bluff": {
            "ability": "charisma",
        },
        "climb": {
            "ability": "strength",
        },
        "craft": {
            "ability": "intelligence",
        },
        "diplomacy": {
            "ability": "charisma",
        },
        "disable device": {
            "ability": "dexterity",
        },
        "disguise": {
            "ability": "charisma",
        },
        "escape artist": {
            "ability": "dexterity",
        },
        "fly": {
            "ability": "dexterity",
        },
        "handle animal": {
            "ability": "charisma",
        },
        "heal": {
            "ability": "wisdom",
        },
        "intimidate": {
            "ability": "charisma",
        },
        "knowledge (arcana)": {
            "ability": "intelligence",
        },
        "knowledge (dungeoneering)": {
            "ability": "intelligence",
        },
        "knowledge (engineering)": {
            "ability": "intelligence",
        },
        "knowledge (geography)": {
            "ability": "intelligence",
        },
        "knowledge (history)": {
            "ability": "intelligence",
        },
        "knowledge (local)": {
            "ability": "intelligence",
        },
        "knowledge (nature)": {
            "ability": "intelligence",
        },
        "knowledge (nobility)": {
            "ability": "intelligence",
        },
        "knowledge (planes)": {
            "ability": "intelligence",
        },
        "knowledge (religion)": {
            "ability": "intelligence",
        },
        "linguistics": {
            "ability": "intelligence",
        },
        "perception": {
            "ability": "wisdom",
        },
        "perform": {
            "ability": "charisma",
        },
        "profession": {
            "ability": "wisdom",
        },
        "ride": {
            "ability": "dexterity",
        },
        "sense motive": {
            "ability": "wisdom",
        },
        "sleight of hand": {
            "ability": "dexterity",
        },
        "spellcraft": {
            "ability": "intelligence",
        },
        "stealth": {
            "ability": "dexterity",
        },
        "survival": {
            "ability": "wisdom",
        },
        "swim": {
            "ability": "strength",
        },
        "use magic device": {
            "ability": "charisma",
        },
    }

def calculate(s: dict, effect_total: int = 0):
    ranks = s.get("ranks", 0)
    is_class = s.get("class", False)
    has_ranks = ranks > 0

    class_bonus = 3 if has_ranks and is_class else 0

    modifier = ranks + class_bonus + effect_total

    s["modifier"] = modifier
