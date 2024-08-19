import argparse
import json
import sys

from rerole_lib import character as c, utils

_output_formats = ["text", "json"]

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        type=str,
        help="Path to character data file.",
    )
    parser.add_argument(
        "--format", "-f",
        choices=_output_formats,
        default=_output_formats[0],
        help="Output format",
    )

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    filepath = args.filename
    with open(filepath) as f:
        data = c.load(f)
    calculated = c.calculate(data)
    match args.format:
        case "text":
            abilities = calculated.get("abilities")
            ability_names = abilities.keys()
            name_lengths = [len(x) for x in ability_names]
            longest_ability_name_length = max(name_lengths)
            ability_string = "Abilities:".ljust(longest_ability_name_length)
            ability_string += "\tscore\t\tmodifier"
            print(f"\n{ability_string}")
            print("----------")
            for name in ability_names:
                ability = abilities.get(name)
                if not ability:
                    continue
                padded_name = name.ljust(longest_ability_name_length)
                score = ability.get("score", 0)
                modified_score = ability.get("modified_score", 0)
                modifier = ability.get("modifier", 0)
                print(f"{padded_name}\t{score}\t{modified_score}\t{modifier}")

            skills = calculated.get("skills")
            skill_names = skills.keys()
            name_lengths = [len(x) for x in skill_names]
            longest_skill_name_length = max(name_lengths)
            skill_string = "Skills:".ljust(longest_skill_name_length)
            skill_string += "\tranks" + "\tability".ljust(longest_ability_name_length) + "\tclass\tmodifier"
            print(f"\n{skill_string}")
            print("-------")
            for name in skill_names:
                skill = skills.get(name)
                if not skill:
                    continue
                padded_name = name.ljust(longest_skill_name_length)
                ranks = skill.get("ranks", 0)
                ability_name = skill.get("ability", "").ljust(longest_ability_name_length)
                is_class = "*" if skill.get("class", False) else " "
                modifier = skill.get("modifier", 0)
                print(f"{padded_name}\t{ranks}\t{ability_name}\t{is_class}\t{modifier}")
        case "json":
            print(json.dumps(calculated, indent=4))
        case _:
            print(f"Unhandled output format: {args.format}.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
