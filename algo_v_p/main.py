from SignalingGame import SignalingGame
from display_2types import display_2types_g, display_2types_BNE

T = ["H", "L"]       # Types de l'émetteur : Haut et Bas
S = ["S1", "S2", "S3"]  # Signaux possibles
A = ["A1", "A2", "A3"]  # Actions possibles du récepteur


def Us(t, s, a):
    tot = 0
    # L'émetteur préfère certaines actions du récepteur
    if a == "A3":
        tot += 2
    # Bonus si le signal correspond au type (exemple simple)
    if (t == "H" and s == "S1") or (t == "L" and s == "S2"):
        tot += 1
    return tot


def Ur(t, s, a):
    # Le récepteur gagne si l'action correspond au type réel
    if (t == "H" and a == "A1") or (t == "L" and a == "A3"):
        return 1
    return 0


G = SignalingGame(T, S, A, Us, Ur)
display_2types_g(G, 0, 5, display_ir=True)
display_2types_BNE(G, 0, 5)
