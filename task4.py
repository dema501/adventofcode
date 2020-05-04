import string

def decodeName(name, room):
    alphabet = string.ascii_lowercase
    step = room%len(alphabet)

    nameParts = name.split("-")

    for i, n in enumerate(nameParts):
        convertedName = ""
        for c in n.lower():
            idx = alphabet.index(c)
            needIdx = (idx + step)%len(alphabet)
            convertedName = convertedName + alphabet[needIdx]

        nameParts[i] = convertedName

    return " ".join(nameParts)


def getRoom(code):
    codeParts = code.split("-")

    name = "".join(codeParts[:-1])
    id = codeParts[-1].split('[')[0]
    checksum = codeParts[-1].split('[')[-1][:-1]

    uniq=dict(zip(list(name), [list(name).count(i) for i in list(name)] ))

    tl = sorted(uniq.items(), key = lambda kv:(-kv[1], kv[0]))

    calcChecksum = "".join([t[0] for t in tl])[:5]

    return  calcChecksum, id, checksum, "-".join(codeParts[:-1])

if __name__ == '__main__':
    cases={
        "aaaaa-bbb-z-y-x-123[abxyz]": "abxyz",
        "a-b-c-d-e-f-g-h-987[abcde]": "abcde",
        "not-a-real-room-404[oarel]": "oarel",
        "totally-real-room-200[decoy]": "loart"
    }

    #run tests
    for line in cases:
        a, b, c, d = getRoom(line)
        assert a == cases[line]


    #production
    answer = 0
    with open("task4.in.txt") as f:
        for line in f:
            a, b, c, d = getRoom(line.strip())
            if a == c:
                answer = answer + int(b)

    print("Answer ==>", answer)

