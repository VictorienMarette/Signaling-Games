from SignalingGame import SignalingGame
from display_2types import display_2types_g, display_2types_BNE

import numpy as np

size_T = 2
size_S = 3
size_A = 5

T = list(range(1, size_T + 1))
S = list(range(1, size_S + 1))
A = list(range(1, size_A + 1))
p = np.random.rand(size_T)
p = p / p.sum()
Us_vec = 10*np.random.rand(size_T * size_S * size_A)
def Us(t, s, a):
    return Us_vec[(t-1) * size_S * size_A + (s-1)*size_A + a-1]
Ur_vec = 10*np.random.rand(size_T * size_S * size_A)
def Ur(t, s, a):
    return Ur_vec[(t-1) * size_S * size_A + (s-1)*size_A + a-1]

G = SignalingGame(T, S, A, Us, Ur)
display_2types_BNE(G, -10, 10)
