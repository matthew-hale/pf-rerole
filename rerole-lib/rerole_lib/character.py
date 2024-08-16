from rerole_lib import utils

def build_effect_index(data: dict) -> dict | None:
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
                    if i not in effect_index.keys():
                        effect_index[i] = []
                    effect_index[i].append(key_seq)
            continue

        if not name:
            continue

        if not isinstance(name, list):
            name = [name]

        for n in name:
            data_item = utils.get_in(data, [group, n])
            if not data_item:
                continue

            if n not in effect_index.keys():
                effect_index[n] = []
            effect_index[n].append(key_seq)

    return effect_index
