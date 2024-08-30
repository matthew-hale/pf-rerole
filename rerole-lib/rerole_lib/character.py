from rerole_lib import ability
from rerole_lib import effect
from rerole_lib import save
from rerole_lib import skill
from rerole_lib.utils import Dict

class Sheet(Dict):
    """`Sheet` is an extention of a standard dictionary that provides some useful methods for working with character sheet data."""

    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
            super().__init__({
                "abilities": ability.default(),
                "saves": save.default(),
                "skills": skill.default(),
            })
            return
        super().__init__(*args, **kwargs)

    def calculate(self):
        """Calulate all relevant character modifiers; modifies in place.

        `calculate` is the main method of the `Sheet` class. Pretty much all relevant functionality is baked into `calculate`, such that it's the only method most users should ever have to call directly.

        `calculate` performs the following operations:

        * Sets the proper state for all magical effects, based on the presence or absence of an antimagic field
        * Creates/updates the effect index
        * Calculates the modifiers of each item within the following groups:
            - Abilities
            - Saves
            - Skills
        """

        antimagic_field_state = self.get("antimagic_field", False)
        self.apply_antimagic_field(antimagic_field_state)

        self.build_effect_index()

        calculate_function = {
            "abilities": ability.calculate,
            "saves": save.calculate,
            "skills": skill.calculate,
        }
        for group in calculate_function:
            for name, item in self.get(group, {}).items():
                # Some things have an ability applied; if this thing does, take that
                # into account here.
                ability_total = 0
                if "ability" in item.keys():
                    a = self.get_in(["abilities", item["ability"]], default={})
                    ability_mod = a.get("modifier", 0)
                    ability_penalty = ability.penalty(a)
                    ability_total = ability_mod + ability_penalty

                effects = self.get_effects(name)
                effect_total = effect.total(effects) + ability_total
                calculate_function[group](item, effect_total)

    def get_effects(self, name: str) -> list[dict]:
        """Searches the effect index, returning the appropriate list of effects for `name`."""
        effect_key_seqs = self.get_in(["effect_index", name], default=[])
        return [self.get_in(seq) for seq in effect_key_seqs]

    def get_effect_sources(self, name: str) -> dict:
        """Searches the effect index, returning the appropriate list of effect sources for `name`.

        Note the difference from `get_effects`: an _effect_ is distinct from an effect _source_.

        Some effect sources contain multiple effects. Consider the following:

            "protection from evil": {
                "description": "Does a whole lot of stuff.",
                "1": {
                    "value": 2,
                    "type": "deflection",
                    "affects": {
                        "saves": True,
                    },
                },
                "2": {
                    "value": 2,
                    "type": "resistance",
                    "affects": {
                        "saves": True,
                    },
                },
            },

        If I call `.get_effects("fortitude")`, I'll get this:

            [
                {
                    "value": 2,
                    "type": "resistance",
                    "affects": {
                        "saves": True,
                    },
                }
            ]

        While useful for performing calculations, sometimes what I actually want is the effect source: the actual spells, feats, etc. being applied. To do this, I have to move up a couple levels in the tree, and return a dictionary containing only the effect sources.
        """
        pass

    def apply_antimagic_field(self, on: bool = False):
        """Apply the proper state to all magical effects, depending on their previous state and the value of the `state` argument; modifies in place.

        Note that this method does not directly interact whatsoever with the "antimagic_field" key: `apply_antimagic_field` receives a boolean value, then applies the proper state to all relevant magical effects.
        """
        search_fn = {
            True: active_magic_effect,
            False: inactive_magic_effect,
        }.get(on)

        effect_key_seqs = self.search(search_fn)
        if not effect_key_seqs:
            return

        for seq in effect_key_seqs:
            e = self.get_in(seq, default={})
            effect.toggle_antimagic_field(e)

    def build_effect_index(self):
        """Finds all effects, and builds an index of `affected_thing->effect key seq`.

        This function assumes that names of things are globally unique. If a character has an ability called "strength" and a skill called "strength", the resulting effect index will squish them together into a single entry.

        In practice, things which have effects applied to them generally have globally unique names, as they're things like abilities, saving throws, skills, and various built-in rolls, like AC and spellcasting concentration checks.
        """
        if "effect_index" in self:
            del self["effect_index"]

        effects = self.search(lambda x: isinstance(x, dict) and "affects" in x.keys())
        if not effects:
            return

        effect_index = Dict()
        for key_seq in effects:
            effect = self.get_in(key_seq)
            if not effect:
                continue

            affecting_rules = effect["affects"]

            for group, value in affecting_rules.items():
                type_ = type(value)
                if type_ is bool and value is True:
                    for item in self.get(group, {}).keys():
                        effect_index.add_or_append(item, key_seq)
                elif type_ is str:
                    effect_index.add_or_append(value, key_seq)
                elif type_ is list:
                    for item in value:
                        effect_index.add_or_append(item, key_seq)
                else:
                    continue

        self["effect_index"] = effect_index


def active_magic_effect(e: dict) -> bool:
    return isinstance(e, dict) and effect.active(e) and e.get("magic", False)

def inactive_magic_effect(e: dict) -> bool:
    return isinstance(e, dict) and effect.inactive(e) and e.get("magic", False)
