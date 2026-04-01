import numpy as np
import itertools

from .polyhedrons import h_rep_to_v_rep


class SignalingGame_CE_calculations:
    def __init__(self, T, S, A, Us, Ur):
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

    def get_ce_vertexes_for_deviation_punish(self, p, nu):
        conditions = self.__get_ce_conditions_for_dp(p, nu)
        CE_v_rep, _, _ = h_rep_to_v_rep(conditions[0], conditions[1])
        return CE_v_rep

    def print_ce_outcome_for_deviation_punish(self, p, nu):
        vertexes = self.get_ce_vertexes_for_deviation_punish(p, nu)
        print("Vertex of outcome space for ", end="")
        self.print_deviation_punish(nu)
        i = 1
        for v in vertexes:
            print("Vertexe " + str(i), end="")
            self.print_outcome(p, v)
            i += 1

    def print_outcome(self, p, x, end="\n"):
        text = ""
        for t in self.T:
            for s in self.S:
                for a in self.A:
                    text += " pi("+s+","+a+"|"+t+")=" + \
                            str(round(float(x[self.TxSxA_to_int(t, s, a)]), 6))
        print(text+" Us="+str(round(self.E_Us(p, x), 4))+", Ur="+str(round(self.E_Ur(p, x), 4)),
              end=end)

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

    def E_Us(self, p, x):
        tot = 0
        for t in self.T:
            ti = self.T.index(t)
            for a in self.A:
                for s in self.S:
                    index = self.TxSxA_to_int(t, s, a)
                    tot += p[ti]*x[index]*self.Us(t, s, a)
        return tot

    def E_Ur(self, p, x):
        tot = 0
        for t in self.T:
            ti = self.T.index(t)
            for a in self.A:
                for s in self.S:
                    index = self.TxSxA_to_int(t, s, a)
                    tot += p[ti]*x[index]*self.Ur(t, s, a)
        return tot

    def __get_ce_conditions_for_dp(self, p, nu, get_parameters=False):
        return (self.__get_ce_ineqs_prob_for_dp(get_parameters)
                + self.__get_ce_ineqs_sender_for_dp(nu, get_parameters)
                + self.__get_ce_ineqs_recevier_for_dp(p, nu, get_parameters),
                self.__get_ce_eqs_prob_for_dp(get_parameters))

    def __get_ce_eqs_prob_for_dp(self, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        eqs = []
        for t in range(lT):
            v = np.zeros(lT*lS*lA + 1)
            v[0] = -1
            v[t*lS*lA+1:(t+1)*lS*lA+1] = 1
            if get_parameters:
                eqs.append((v, self.T[t]))
            else:
                eqs.append(v)
        return eqs

    def __get_ce_ineqs_prob_for_dp(self, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        ineqs = []
        for i in range(lT*lS*lA):
            v = np.zeros(lT*lS*lA+1)
            v[1+i] = 1
            if get_parameters:
                ineqs.append((v, self.int_to_TxSxA(i)))
            else:
                ineqs.append(v)
        return ineqs

    def __get_ce_ineqs_sender_for_dp(self, nu, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        SS_funcs = list(itertools.product(self.S, repeat=lS))
        ineqs = []
        for t, t2, f in itertools.product(self.T, self.T, SS_funcs):
            v = np.zeros(lT*lS*lA+1)
            for s, a in itertools.product(self.S, self.A):
                si = self.S.index(s)
                v[self.TxSxA_to_int(t, s, a)+1] += self.Us(t, s, a)
                if f[si] == s:
                    v[self.TxSxA_to_int(t2, s, a)+1] += -self.Us(t, s, a)
                else:
                    v[self.TxSxA_to_int(t2, s, a)+1] += -self.__E_Us_of_dp(nu, t, s, f[si])
            if get_parameters:
                ineqs.append((v, (t, t2, f)))
            else:
                ineqs.append(v)
        return ineqs

    def __get_ce_ineqs_recevier_for_dp(self, p, nu, get_parameters=False):
        lT = len(self.T)
        lS = len(self.S)
        lA = len(self.A)
        AA_funcs = list(itertools.product(self.A, repeat=lS))
        ineqs = []
        for s, s2, f in itertools.product(self.S, self.S, AA_funcs):
            v = np.zeros(lT*lS*lA+1)
            for t, a in itertools.product(self.T, self.A):
                ti = self.T.index(t)
                ai = self.A.index(a)
                v[self.TxSxA_to_int(t, s, a)+1] += p[ti]*self.Ur(t, s, a)
                if s == s2:
                    v[self.TxSxA_to_int(t, s, a)+1] += -p[ti]*self.Ur(t, s, f[ai])
                else:
                    v[self.TxSxA_to_int(t, s, a)+1] += -p[ti] * \
                        nu[self.__dp_TxSXSxA_to_int(t, s, s2, a)]*self.Ur(t, s, f[ai])
            if get_parameters:
                ineqs.append((v, (s, a, f)))
            else:
                ineqs.append(v)
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

    def __E_Us_of_dp(self, nu, t, s, s2):
        tot = 0
        for a in self.A:
            tot += nu[self.__dp_TxSXSxA_to_int(t, s, s2, a)]*self.Us(t, s2, a)
        return tot
