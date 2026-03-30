# Types
T = ["W", "S", "X", "Y"]  # maintenant 4 types
S = ["B", "Q"]
A = ["F", "C"]


# Fonction de payoff pour le joueur 1
def Us(t, s, a):
    tot = 0
    if a == "C":
        tot += 2
    # Bonus selon combinaisons T-S
    if (t == "W" and s == "Q") or (t == "S" and s == "B"):
        tot += 1
    if (t == "X" and s == "B") or (t == "Y" and s == "Q"):
        tot += 1
    return tot


# Fonction de payoff pour le joueur 2
def Ur(t, s, a):
    tot = 0
    # Bonus selon combinaisons T-A
    if (t == "W" and a == "F") or (t == "S" and a == "C"):
        tot += 1
    if (t == "X" and a == "C") or (t == "Y" and a == "F"):
        tot += 1
    return tot
