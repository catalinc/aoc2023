import sys


def get_day_input(day: int) -> list[str]:
    with open(_get_input_filename(day), encoding="utf-8") as infile:
        return [line.strip() for line in infile]


def _get_input_filename(day: int) -> str:
    is_test = "-t" in sys.argv
    suffix = ""
    if is_test:
        suffix = "_test"
        if len(sys.argv) == 3:
            suffix += sys.argv[2]
    return f"input/day{day}{suffix}.txt"


def get_day_input_full_content(day: int) -> str:
    with open(_get_input_filename(day), encoding="utf-8") as infile:
        return infile.read()


def chunks(lst, size: int):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]
