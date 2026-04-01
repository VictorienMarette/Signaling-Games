import numpy as np

from .SignalingGame import SignalingGame


class ClearPunishSignalingGame(SignalingGame):

    def __init__(self, T, S, A, Us, Ur, P=None):
        super().__init__(T, S, A, Us, Ur)
        if P is None:
            self.P = ClearPunishSignalingGame.get_clear_punish(T, S, A, Us)
            if self.P is None:
                raise ValueError("G doesn't have clear punishment")
        else:
            self.P = P
            if not self.chek_punish():
                raise ValueError("P isn't a clear punish")

    def chek_punish(self):
        if self.P is None:
            return False
        for t in self.T:
            for s in self.S:
                for a in self.A:
                    if self.Us(t, s, a) < self.Us(t, s, self.P(s)):
                        return False
        return True

    def CE_outcome_v_rep(self, p):
        i = 0
        nu = np.zeros(len(self.A)*len(self.T)*len(self.S)*(len(self.S)-1))  
        for t in self.T:
            for s in self.S:
                for s2 in self.S:
                    if s != s2:
                        for a in self.A:
                            if a == self.P(s2):
                                nu[i] = 1
                            i += 1
        return self.CE_outcome_v_rep_for_deviation_punish(p, nu)

    def print_CE_outcome(self, p):
        vertexes = self.CE_outcome_v_rep(p)
        print("Vertex of outcome space:")
        i = 1
        for v in vertexes:
            print("Vertexe " + str(i), end="")
            self.print_outcome(p, v)
            i += 1

    @staticmethod
    def get_clear_punish(T, S, A, Us):
        def get_cp(s):
            for a in A:
                if is_cp(s, a):
                    return a
            return None

        def is_cp(s, a):
            for t in T:
                for a2 in A:
                    if Us(t, s, a) > Us(t, s, a2):
                        return False
            return True

        Punishs = {}
        for s in S:
            p = get_cp(s)
            if p is None:
                return None
            Punishs[s] = p

        def P(s):
            return Punishs[s]

        return P

    @classmethod
    def generate_random(cls, size_T, size_S, size_A):
        T = list(range(1, size_T + 1))
        S = list(range(1, size_S + 1))
        A = list(range(1, size_A + 1))
        p = np.random.rand(size_T)
        p = p / p.sum()
        P = None
        i = 0
        while P is None:
            Us_vec = 10*np.random.rand(size_T * size_S * size_A)

            def Us(t, s, a, offset=i):
                return Us_vec[(t-1) * size_S * size_A + (s-1)*size_A + a-1]

            Ur_vec = 10*np.random.rand(size_T * size_S * size_A)

            def Ur(t, s, a, offset=i):
                return Ur_vec[(t-1) * size_S * size_A + (s-1)*size_A + a-1]

            P = cls.get_clear_punish(T, S, A, Us)
            i += 1
        return cls(p, T, S, A, Us, Ur, P)