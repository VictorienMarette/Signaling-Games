from SignalingGame import SignalingGame
from display_2types import display_2types_BNE

# Types, Signaux et Actions
T = ["Faim", "Satié"]   # Types de l'envoyeur
S = ["Silence", "Cri"]  # Signaux possibles
A = ["Fuir", "Sapprocher", "Piège"]  # Actions du récepteur


# Utilité de l'envoyeur (U_s)
def Us(t, s, a):
    tot = 0
    # L'envoyeur aime obtenir de la nourriture
    if t == "Faim" and a == "Sapprocher":
        tot += 3
    if t == "Satié" and a != "Piège":
        tot += 2
    # Le signal peut influencer légèrement
    if (t == "Faim" and s == "Cri") or (t == "Satié" and s == "Silence"):
        tot += 1
    return tot


# Utilité du récepteur (U_r)
def Ur(t, s, a):
    # Le récepteur gagne s'il devine correctement le type
    if (t == "Faim" and a == "Piège") or (t == "Satié" and a == "Sapprocher"):
        return 2
    if (t == "Faim" and a == "Fuir") or (t == "Satié" and a == "Fuir"):
        return 1
    return 0


G = SignalingGame(T, S, A, Us, Ur)
display_2types_BNE(G, 0, 4)