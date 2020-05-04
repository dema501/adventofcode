def calcDirection(d, s):
    if d == "N" and s == "L":
        return "W", "x-"
    if d == "N" and s == "R":
        return "E", "x+"

    if d == "E" and s == "L":
        return "N", "y+"
    if d == "E" and s == "R":
        return "S", "y-"

    if d == "S" and s == "L":
        return "E", "x+"
    if d == "S" and s == "R":
        return "W", "x-"

    if d == "W" and s == "L":
        return "S", "y-"
    if d == "W" and s == "R":
        return "N", "y+"


def calcDistance(p):
    x, y = 0, 0
    direction = "N"
    # uniq_coords = set()

    for i, step in enumerate(p.split(", ")):
        direction, op = calcDirection(direction, step[0])
    
        if "x-" in op:
            x = x - int(step[1:])
        elif "x+" in op:
            x = x + int(step[1:])
        elif "y-" in op:
            y = y - int(step[1:])
        elif "y+" in op:
            y = y + int(step[1:])

    return x, y


def calcPath(p):
    x, y = 0, 0
    direction = "N"
    uniq_coords = ["(0, 0)"]

    for i, step in enumerate(p.split(", ")):
        direction, op = calcDirection(direction, step[0])
    
        # print(step, direction, op, i)
        for j in range(0, int(step[1:])):
            if "x-" in op:
                x = x - 1
            elif "x+" in op:
                x = x + 1
            elif "y-" in op:
                y = y - 1
            elif "y+" in op:
                y = y + 1

            cord = "({}, {})".format(x, y)

            if cord not in uniq_coords:
                uniq_coords.append(cord)
            else:
                return x, y, i+1


    return x, y, i+1

if __name__ == '__main__':
    cases={
        """R5, L5, R5, R3""": 12,
        """R8, R4, R4, R8""": 4,
        """R2, R2, R5, R4, L2, R1, R3, R4, L3, L5, R2, R2, R3""": 1,
        """L2, R2, L3, R2, R5, R7, R1, R6, L1, R3""": 0,
    }

    #run tests
    for k in cases:
        x, y, i = calcPath(k)
        assert (abs(x) + abs(y)) == cases[k]


    #production
    with open("task1.in.txt") as f:
        content = f.read()
        x, y, i = calcPath(content.strip())

        print("Answer", abs(x) + abs(y))
