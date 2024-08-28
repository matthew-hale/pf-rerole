from rerole_lib import ability
from rerole_lib import effect
from rerole_lib import save
from rerole_lib import skill
from rerole_lib import utils

def default() -> dict:
    """Create a new blank character sheet"""
    return {
        "abilities": ability.default(),
        "saves": save.default(),
        "skills": skill.default(),
    }

def calculate(data: dict) -> dict:
    """Calulate all relevant modifiers, returning a new dict."""
    antimagic_field_is_on = data.get("antimagic_field", False)
    if antimagic_field_is_on:
        activate_antimagic_field(data)
    else:
        deactivate_antimagic_field(data)

    update_effect_index(data)
    effect_index = data.get("effect_index", {})

    for k, v in data.get("abilities", {}).items():
        ability_effects = resolve_effect_index(data, k)
        effect_total = effect.total(ability_effects)
        ability.calculate(v, effect_total)

    for k, v in data.get("saves", {}).items():
        save_effects = resolve_effect_index(data, k)
        save_effect_total = effect.total(save_effects)

        save_ability = utils.get_in(data, ["abilities", v.get("ability")], {})
        save_ability_modifier = save_ability.get("modifier", 0)
        save_ability_penalty = ability.penalty(save_ability)

        effect_total = save_effect_total + save_ability_modifier + save_ability_penalty
        save.calculate(v, effect_total)

    for k, v in data.get("skills", {}).items():
        skill_effects = resolve_effect_index(data, k)
        skill_effect_total = effect.total(skill_effects)

        skill_ability = utils.get_in(data, ["abilities", v.get("ability")], {})
        skill_ability_modifier = skill_ability.get("modifier", 0)
        skill_ability_penalty = ability.penalty(skill_ability)

        effect_total = skill_effect_total + skill_ability_modifier + skill_ability_penalty
        skill.calculate(v, effect_total)


def activate_antimagic_field(data: dict):
    """Apply the proper suppression state to each magical effect present."""
    active_magic_effect_key_seqs = utils.search(data, active_magic_effect)
    if not active_magic_effect_key_seqs:
        return

    for seq in active_magic_effect_key_seqs:
        e = utils.get_in(data, seq, {})
        effect.toggle_antimagic_field(e)

def deactivate_antimagic_field(data: dict):
    """Like activate_antimagic_field, but in reverse."""
    inactive_magic_effect_key_seqs = utils.search(data, inactive_magic_effect)
    if not inactive_magic_effect_key_seqs:
        return

    for seq in inactive_magic_effect_key_seqs:
        e = utils.get_in(data, seq, {})
        effect.toggle_antimagic_field(e)


def update_effect_index(data: dict):
    """Add an up-to-date effect index to the provided character dict."""
    effect_index = build_effect_index(data)
    if not effect_index:
        return

    data["effect_index"] = effect_index

def build_effect_index(data: dict) -> dict:
    """Finds all effects in character data, and builds an index of things->effect key sequences.

    This function assumes that names of things are globally unique. If a character has an ability called 'strength' and a skill called 'strength', the resulting effect index will squish them together into a single entry.

    In practice, things which have effects applied to them generally have globally unique names, as they're things like abilities, saving throws, skills, and various built-in rolls, like AC and spellcasting concentration checks.
    """
    effects = utils.search(data, lambda x: isinstance(x, dict) and "affects" in x.keys())

    if not effects:
        return {}

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
    """Return a list of effects that are affecting the named item."""
    effect_key_seqs = utils.get_in(data, ["effect_index", name])
    if not effect_key_seqs:
        return []

    return [utils.get_in(data, seq) for seq in effect_key_seqs]


def active_magic_effect(e: dict) -> bool:
    return isinstance(e, dict) and effect.active(e) and e.get("magic", False)

def inactive_magic_effect(e: dict) -> bool:
    return isinstance(e, dict) and effect.inactive(e) and e.get("magic", False)
