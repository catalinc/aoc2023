def get_day_input(day: int) -> list[str]:
    with open(f"input/day{day}.txt",  encoding="utf-8") as infile:
        return [line.strip() for line in infile]

