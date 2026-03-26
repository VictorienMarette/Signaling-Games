import numpy as np
from polyhedrons import h_rep_to_v_rep, v_rep_to_h_rep, canonicalize_h_rep


class SignalingGame:
    def __init__(self, T, S, A, Us, Ur):
        self.T = T
        self.S = S
        self.A = A
        self.Us = Us
        self.Ur = Ur

    def ir_h_rep(self):
        ir_ineq = []
        ir_eq = []
        for s in self.S:
            irs_ineq, irs_eq = self.__irs_h_rep(s)
            ir_ineq.extend(irs_ineq)
            ir_eq.extend(irs_eq)
        return canonicalize_h_rep(ir_ineq, ir_eq)

    def pk_v_rep(self, s, Tt, At):
        ineq, eq = self.__pk_h_rep(s, Tt, At)
        return h_rep_to_v_rep(ineq, eq)

    def Us_index(self, t, s, a, t_index=True, s_index=True, a_index=True):
        if t_index:
            t = self.T[t]
        if s_index:
            s = self.S[s]
        if a_index:
            a = self.A[a]
        return self.Us(t, s, a)

    def Ur_index(self, t, s, a, t_index=True, s_index=True, a_index=True):
        if t_index:
            t = self.T[t]
        if s_index:
            s = self.S[s]
        if a_index:
            a = self.A[a]
        return self.Ur(t, s, a)

    def __irs_h_rep(self, s):
        # We define the H-rep of VY to get his V-rep for the vec (vt1, ..., vtn, y(a1), ..., y(an))
        # [There is a better methode]
        ineq_vy = []
        eq_vy = []
        lT = len(self.T)
        lA = len(self.A)
        # 0 <= y(ai)
        for i in range(lA):
            ineq = np.zeros(1 + lT + lA)
            ineq[1 + lT + i] = 1
            ineq_vy.append(ineq)
        # 0 = -1 + sum_i y(ai)
        eq = np.zeros(1 + lT + lA)
        eq[0] = -1
        for i in range(lA):
            eq[1 + lT + i] = 1
        eq_vy.append(eq)
        # 0 <= vt + sum_i y(ai)Us(t,s,ai)
        for i in range(lT):
            ineq = np.zeros(1 + lT + lA)
            ineq[1 + i] = 1
            for ia in range(lA):
                ineq[1 + lT + ia] = -self.Us_index(i, s, ia, s_index=False)
            ineq_vy.append(ineq)

        # Get the V-rep of VY
        V, R, L = h_rep_to_v_rep(ineq_vy, eq_vy)

        # Get the V-rep on Ir
        V2 = [v[:lT] for v in V]
        R2 = [r[:lT] for r in R]
        L2 = [le[:lT] for le in L]

        return v_rep_to_h_rep(V2, R2, L2)

    def __pk_h_rep(self, s, Tt, At):
        # Tt are indexes of T and At are indexes of A
        ineq_p = []
        eq_p = []
        lT = len(self.T)
        lA = len(self.A)
        # 0 <= p(ti) for ti in Tt
        for i in Tt:
            ineq = np.zeros(1+lT)
            ineq[1+i] = 1
            ineq_p.append(ineq)
        # 0 = p(ti) for ti not in Tt
        for i in range(lT):
            if i not in Tt:
                eq = np.zeros(1+lT)
                eq[1+i] = 1
                eq_p.append(eq)
        # 1 = sum p(t)
        eq = np.zeros(1+lT)
        eq[0] = -1
        for i in range(lT):
            eq[1+i] = 1
        eq_p.append(eq)
        # sum p(t)Us(t,s,a1)=sum p(t)Us(t,s,a) for all a in At
        ia1 = At[0]
        for ia in At[1:]:
            eq = np.zeros(1+lT)
            for it in Tt:
                eq[1+it] += self.Ur_index(it, s, ia, s_index=False)
                eq[1+it] += -self.Ur_index(it, s, ia1, s_index=False)
            eq_p.append(eq)
        # sum p(t)Us(t,s,a1)>=sum p(t)Us(t,s,a) for all a not in At
        for ia in range(lA):
            if ia not in At:
                ineq = np.zeros(1+lT)
                for it in Tt:
                    ineq[1+it] += self.Ur_index(it, s, ia1, s_index=False)
                    ineq[1+it] += -self.Ur_index(it, s, ia, s_index=False)
                ineq_p.append(ineq)
        return ineq_p, eq_p
