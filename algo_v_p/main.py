from SignalingGame import SignalingGame
from display_2types import display_2types_g


T = ["W", "S"]
S = ["B", "Q"]
A = ["F", "C"]


def Us(t, s, a):
    tot = 0
    if a == "C":
        tot += 2
    if (t == "W" and s == "Q") or (t == "S" and s == "B"):
        tot += 1
    return tot


def Ur(t, s, a):
    if (t == "W" and a == "F") or (t == "S" and a == "C"):
        return 1
    return 0


G = SignalingGame(T, S, A, Us, Ur)
display_2types_g(G, 0, 4, ir_constrained=True, display_ir=False)