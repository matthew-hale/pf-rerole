from rerole_lib import utils

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
        if isinstance(group, list):
            for g in group:
                data_group = data.get(g)
                if not data_group:
                    continue

                items = data_group.keys()
                for i in items:
                    utils.add_or_append(effect_index, i, key_seq)
            continue

        if not name:
            continue

        if not isinstance(name, list):
            name = [name]

        for n in name:
            data_item = utils.get_in(data, [group, n])
            if not data_item:
                continue

            utils.add_or_append(effect_index, n, key_seq)

    return effect_index
