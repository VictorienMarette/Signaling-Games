import numpy as np
import itertools

from simplex import vertexes, in_simplex


class SignalingGame:
    def __init__(self, p, T, S, A, Us, Ur):
        self.p = p
        self.T = T
        self.S = S
        self.A = A
        self.Us = Us
        self.Ur = Ur

    def TxSxA_to_int(self, t, s, a):
        lS = len(self.S)
        lA = len(self.A)
        ti = self.T.index(t)
        si = self.S.index(s)
        ai = self.A.index(a)
        return ti*lS*lA + si*lA + ai

    def int_to_TxSxA(self, i):
        lS = len(self.S)
        lA = len(self.A)
        ti, r = divmod(i, lS*lA)
        si, ai = divmod(r, lA)
        return (self.T[ti], self.S[si], self.A[ai])

    def is_outcome_ce(self, x):
        pass

    def is_outcome_bn_with_cheaptalk(self, x, eps=1e-12):
        if False:
            raise ValueError("x should be probas for each t")
        return False

    def get_ce_vertexes_for_deviation_punish(self, nu):
        conditions = self.__get_ce_conditions_for_dp(nu)
        return vertexes(conditions[0], conditions[1])

    def print_ce_outcome_for_deviation_punish(self, nu):
        vertexes = self.get_ce_vertexes_for_deviation_punish(nu)
        print("Vertex of outcome space for ", end="")
        self.print_deviation_punish(nu)
        i = 1
        for v in vertexes:
            print("Vertexe " + str(i), end="")
            self.print_outcome(v)
            i += 1

    def print_outcome(self, x, end="\n"):
        text = ""
        for t in self.T:
            for s in self.S:
                for a in self.A:
                    text += " pi("+s+","+a+"|"+t+")=" + str(round(float(x[self.TxSxA_to_int(t, s, a)]), 6))
        print(text+" Us="+str(round(self.E_Us(x), 4))+", Ur="+str(round(self.E_Ur(x), 4)), end=end)

    def print_deviation_punish(self, nu, end="\n"):
        text = ""
        i = 0
        for t in self.T:
            for s in self.S:
                for s2 in self.S:
                    if s != s2:
                        for a in self.A:
                            text += " nu("+a+"|"+t+", "+s+", "+s2+")=" + str(round(float(nu[i]), 6))
                            i += 1
        print(text, end=end)

    def E_Us(self, x):
        tot = 0
        for t in self.T:
            ti = self.T.index(t)
            for a in self.A:
                for s in self.S:
                    index = self.TxSxA_to_int(t, s, a)
                    tot += self.p[ti]*x[index]*self.Us(t, s, a)
        return tot

    def E_Ur(self, x):
        tot = 0
        for t in self.T:
            ti = self.T.index(t)
            for a in self.A:
                for s in self.S:
                    index = self.TxSxA_to_int(t, s, a)
                    tot += self.p[ti]*x[index]*self.Ur(t, s, a)
        return tot

    def __str__(self):
        txt = "SignalingGame:\n"
        txt += f"  T = {self.T}\n"
        txt += f"  S = {self.S}\n"
        txt += f"  A = {self.A}\n"
        txt += f"  p = {self.p}\n\n"

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

    def __get_ce_conditions_for_dp(self, nu, get_parameters=False):
        return (self.__get_ce_ineqs_prob_for_dp(get_parameters)
                + self.__get_ce_ineqs_sender_for_dp(nu, get_parameters)
                + self.__get_ce_ineqs_recevier_for_dp(nu, get_parameters), 
                self.__get_ce_eqs_prob_for_dp(get_parameters))

    def __get_ce_eqs_prob_for_dp(self, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        eqs = []
        for t in range(lT):
            v = np.zeros(lT*lS*lA)
            v[t*lS*lA:(t+1)*lS*lA] = 1
            if get_parameters:
                eqs.append((v, 1, self.T[t]))
            else:
                eqs.append((v, 1))
        return eqs

    def __get_ce_ineqs_prob_for_dp(self, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        ineqs = []
        for i in range(lT*lS*lA):
            v = np.zeros(lT*lS*lA)
            v[i] = -1
            if get_parameters:
                ineqs.append((v, 0, self.int_to_TxSxA(i)))
            else:
                ineqs.append((v, 0))
        return ineqs

    def __get_ce_ineqs_sender_for_dp(self, nu, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        SS_funcs = list(itertools.product(self.S, repeat=lS))
        ineqs = []
        for t, t2, f in itertools.product(self.T, self.T, SS_funcs):
            v = np.zeros(lT*lS*lA)
            for s, a in itertools.product(self.S, self.A):
                si = self.S.index(s)
                v[self.TxSxA_to_int(t, s, a)] += -self.Us(t, s, a)
                if f[si] == s:
                    v[self.TxSxA_to_int(t2, s, a)] += self.Us(t, s, a)
                else:
                    v[self.TxSxA_to_int(t2, s, a)] += self.__E_Us_of_dp(nu, t, s, f[si])
            if get_parameters:
                ineqs.append((v, 0, (t, t2, f)))
            else:
                ineqs.append((v, 0))
        return ineqs

    def __get_ce_ineqs_recevier_for_dp(self, nu, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        AA_funcs = list(itertools.product(self.A, repeat=lS))
        ineqs = []
        for s, s2, f in itertools.product(self.S, self.S, AA_funcs):
            v = np.zeros(lT*lS*lA)
            for t, a in itertools.product(self.T, self.A):
                ti = self.T.index(t)
                ai = self.A.index(a)
                v[self.TxSxA_to_int(t, s, a)] += -self.p[ti]*self.Ur(t, s, a)
                if s == s2:
                    v[self.TxSxA_to_int(t, s, a)] += self.p[ti]*self.Ur(t, s, f[ai])
                else:
                    v[self.TxSxA_to_int(t, s, a)] += self.p[ti]*nu[self.__dp_TxSXSxA_to_int(t, s, s2, a)]*self.Ur(t, s, f[ai])
            if get_parameters:
                ineqs.append((v, 0, (s, a, f)))
            else:
                ineqs.append((v, 0))
        return ineqs

    def __dp_TxSXSxA_to_int(self, t, s, s2, a):
        lS = len(self.S)
        lA = len(self.A)
        ti = self.T.index(t)
        si = self.S.index(s)
        s2i = self.S.index(s2)
        ai = self.A.index(a)
        if s2i < si:
            return ti*lS*(lS-1)*lA + si*(lS-1)*lA + s2i*lA + ai
        elif s2i > si:
            return ti*lS*(lS-1)*lA + si*(lS-1)*lA + (s2i-1)*lA + ai
        return None

    def __dp_int_to_TxSxSxA(self, i):
        pass
        """lS = len(self.S)
        lA = len(self.A)
        ti, r = divmod(i, lS*lA)
        si, ai = divmod(r, lA)
        return (self.T[ti], self.S[si], self.A[ai])"""

    def __E_Us_of_dp(self, nu, t, s, s2):
        tot = 0
        for a in self.A:
            tot += nu[self.__dp_TxSXSxA_to_int(t, s, s2, a)]*self.Us(t, s2, a)
        return tot