import random, re

def main() :
    with open("input.txt", 'r') as f:
        data = f.readlines()

    data = [i.strip() for i in data]

    print(data)
    dataset = set()

    while len(dataset) < 25:
        dataset.add(random.choice(data))

    return list(dataset)

def GenText(inlist: list[str]) -> list[str]:
    dataset = set()

    if len(inlist) > 25:
        while len(dataset) < 25:
            dataset.add(random.choice(inlist))


    return list(dataset)


def GenColors() -> (list[str], bool):
    colors = ["black"]
    colors.extend(["red" for i in range(8)])
    colors.extend(["lightblue" for i in range(8)])
    colors.extend(["lightgray" for i in range(7)])
    # Random last color, for which team goes first
    blue = random.choice([True, False])
    if blue :
        colors.append("lightblue")
    else:
        colors.append("red")

    random.shuffle(colors)

    return colors, blue

def FixInput(instr: str) -> list[str]:
    restr = re.compile("(\n|\r)")
    instr = restr.sub(" ", instr)
    restr = re.compile(" +")
    instr = restr.sub(" ", instr)

    return instr.split(" ")


if __name__ == '__main__':
    main()
