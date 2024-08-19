import json

from copy import deepcopy

from rerole_lib import ability, effect, skill, utils

def load(f):
    data = json.load(f)
    return data

def calculate(data: dict) -> dict:
    out_data = deepcopy(data)
    if not out_data.get("effect_index"):
        out_data = update_effect_index(data)
    effect_index = out_data.get("effect_index", {})

    for k, v in out_data.get("abilities", {}).items():
        ability_effects = resolve_effect_index(out_data, k)
        effect_total = effect.total(ability_effects)
        v = ability.calculate(v, effect_total)
        out_data["abilities"][k] = v

    for k, v in out_data.get("skills", {}).items():
        skill_effects = resolve_effect_index(out_data, k)
        skill_effect_total = effect.total(skill_effects)

        skill_ability_modifier = 0
        skill_ability_penalty = 0
        skill_ability = utils.get_in(out_data, ["abilities", v.get("ability")])
        if skill_ability:
            skill_ability_modifier = skill_ability.get("modifier", 0)
            skill_ability_penalty = ability.penalty(skill_ability)

        effect_total = skill_effect_total + skill_ability_modifier + skill_ability_penalty
        v = skill.calculate(v, effect_total)
        out_data["skills"][k] = v

    return out_data

def update_effect_index(data: dict) -> dict:
    d = deepcopy(data)

    effect_index = build_effect_index(d)
    if not effect_index:
        return d

    d["effect_index"] = effect_index
    return d

def build_effect_index(data: dict) -> dict | None:
    """Finds all effects in character data, and builds an index of things->effect key sequences.

    This function assumes that names of things are globally unique. If a character has an ability called 'strength' and a skill called 'strength', the resulting effect index will squish them together into a single entry.

    In practice, things which have effects applied to them generally have globally unique names, as they're things like abilities, saving throws, skills, and various built-in rolls, like AC and spellcasting concentration checks."""
    effects = utils.search(data, lambda x: isinstance(x, dict) and "affects" in x.keys())

    if not effects:
        return None

    effect_index = {}
    for key_seq in effects:
        effect = utils.get_in(data, key_seq)
        if not effect:
            continue

        affecting_rules = effect["affects"]

        group = affecting_rules.get("group")
        name = affecting_rules.get("name")

        if not group:
            continue

        # If multiple groups, treat "affects" as "everything in these groups"
        multiple_groups = isinstance(group, list)
        if multiple_groups:
            for g in group:
                data_group = data.get(g)
                if not data_group:
                    continue

                items = data_group.keys()
                for i in items:
                    utils.add_or_append(effect_index, i, key_seq)
            continue

        if not name:
            data_group = data.get(group)
            if not data_group:
                continue

            items = data_group.keys()
            for i in items:
                utils.add_or_append(effect_index, i, key_seq)
            continue

        if not isinstance(name, list):
            name = [name]

        for n in name:
            data_item = utils.get_in(data, [group, n])
            if not data_item:
                continue

            utils.add_or_append(effect_index, n, key_seq)

    return effect_index

def resolve_effect_index(data: dict, name: str) -> list[dict]:
    effect_key_seqs = utils.get_in(data, ["effect_index", name])
    if not effect_key_seqs:
        return []

    return [utils.get_in(data, seq) for seq in effect_key_seqs]
