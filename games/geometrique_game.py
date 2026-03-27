import numpy as np

size_T = 2
size_S = 2
size_A = 5

T = list(range(size_T))
S = list(range(size_S))
A = list(range(size_A))


def Us(t, s, a):
    Us_vec = np.array([4.93547844, 2.76927255, 9.57892463, 3.13831285, 1.40434153, 1.89319094,
                       3.81418543, 5.65251674, 1.82479434, 0.43664195, 2.57800177, 2.91399079,
                       2.39241232, 5.11569056, 4.88569773, 6.36679689, 1.09470463, 9.73579971,
                       6.96211307, 9.03248012])
    return Us_vec[(t) * size_S * size_A + (s)*size_A + a]


def Ur(t, s, a):
    Ur_vec = np.array([0.49720147, 0.49928494, 0.78578283, 0.50130029, 0.37247048, 0.45344419,
                       0.09263446, 0.63796919])
    if a < 2:
        a2 = 0
    else:
        a2 = 1
    return Ur_vec[(t) * size_S * 2 + (s)*2 + a2]
