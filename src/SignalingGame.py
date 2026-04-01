import numpy as np

from .SignalingGame_BNE_calculations import SignalingGame_BNE_calculations
from .SignalingGame_CE_calculations import SignalingGame_CE_calculations


class SignalingGame(SignalingGame_BNE_calculations, SignalingGame_CE_calculations):
    def __init__(self, T, S, A, Us, Ur):
        SignalingGame_BNE_calculations.__init__(self, T, S, A, Us, Ur)
        SignalingGame_CE_calculations.__init__(self, T, S, A, Us, Ur)
        self.T = T
        self.S = S
        self.A = A
        self.Us = Us
        self.Ur = Ur

    def g_v_rep(self, include_ir_constraints=True):
        return SignalingGame_BNE_calculations.g_v_rep(
                self, include_ir_constraints=include_ir_constraints)

    def BNE_v_rep(self, Kt_size_limited_by_lenT=True):
        return SignalingGame_BNE_calculations.BNE_v_rep(
                self, Kt_size_limited_by_lenT=Kt_size_limited_by_lenT)

    def CE_outcome_v_rep_for_deviation_punish(self, p, nu):
        pass

    def print_CE_outcome_for_deviation_punish(self, p, nu):
        pass

    def print_CE_deviation_punish(self, nu, end="\n"):
        SignalingGame_CE_calculations.print_deviation_punish(self, nu, end=end)

    def print_outcome(self, p, x, end="\n"):
        SignalingGame_CE_calculations.print_outcome(self, p, x, end=end)

    def __str__(self):
        txt = "SignalingGame:\n"
        txt += f"  T = {self.T}\n"
        txt += f"  S = {self.S}\n"
        txt += f"  A = {self.A}\n\n"
        txt += "  Payoffs Us(t, s, a):\n"
        for t in self.T:
            txt += f"    Type t = {t}:\n"
            for s in self.S:
                # Convert np.float64 -> float
                row = [float(self.Us(t, s, a)) for a in self.A]
                txt += f"      Signal s = {s}: {row}\n"
            txt += "\n"
        txt += "  Payoffs Ur(t, s, a):\n"
        for t in self.T:
            txt += f"    Type t = {t}:\n"
            for s in self.S:
                row = [float(self.Ur(t, s, a)) for a in self.A]
                txt += f"      Signal s = {s}: {row}\n"
            txt += "\n"
        return txt

    @classmethod
    def generate_random(cls, size_T, size_S, size_A):
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
        return cls(p, T, S, A, Us, Ur)
