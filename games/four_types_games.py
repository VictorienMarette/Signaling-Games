T = ["W", "S", "X", "Y"]
S = ["B", "Q"]
A = ["F", "C"]


def Us(t, s, a):
    tot = 0
    if a == "C":
        tot += 2
    if (t == "W" and s == "Q") or (t == "S" and s == "B"):
        tot += 1
    if (t == "X" and s == "B") or (t == "Y" and s == "Q"):
        tot += 1
    return tot


def Ur(t, s, a):
    tot = 0
    if (t == "W" and a == "F") or (t == "S" and a == "C"):
        tot += 1
    if (t == "X" and a == "C") or (t == "Y" and a == "F"):
        tot += 1
    return tot
