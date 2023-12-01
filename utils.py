def get_day_input(day: int, is_test: bool = False) -> list[str]:
    suffix = "" if not is_test else "_test"
    with open(f"input/day{day}{suffix}.txt", encoding="utf-8") as infile:
        return [line.strip() for line in infile]
