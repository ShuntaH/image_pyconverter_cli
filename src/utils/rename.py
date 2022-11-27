import re


def validate_replacement_with_separator_pattern_arg(args):
    if args.replacement_with_separator_pattern:
        return re.compile(
            f"r'{args.replacement_with_separator_pattern}'")
    raise ValueError(
        'replacement_with_separator_pattern option can not be empty.'
    )
