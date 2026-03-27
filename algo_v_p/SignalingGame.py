import numpy as np
from itertools import chain, combinations, product
from functools import lru_cache
from polyhedrons import h_rep_to_v_rep, v_rep_to_h_rep, canonicalize_h_rep, canonicalize_v_rep


def memoize_lists(func):
    """
    Mémoïse une méthode d’instance, transforme automatiquement les listes en tuples.
    Ignore self pour le cache.
    """
    # Création d’un cache séparé
    # La vraie fonction appelée inclut self, mais le cache ignore self
    cached = lru_cache(maxsize=1000)(
        lambda *args, **kwargs: func(*args, **kwargs)
    )

    def wrapper(self, *args, **kwargs):
        # transforme les listes en tuples dans args
        hashable_args = tuple(tuple(a) if isinstance(a, list) else a for a in args)
        # transforme les listes en tuples dans kwargs et trie pour ordre stable
        hashable_kwargs = tuple(
            (k, tuple(v) if isinstance(v, list) else v)
            for k, v in sorted(kwargs.items())
        )
        # Appelle la vraie fonction en incluant self
        return cached(self, *hashable_args, **dict(hashable_kwargs))

    return wrapper


class SignalingGame:
    def __init__(self, T, S, A, Us, Ur):
        self.T = T
        self.S = S
        self.A = A
        self.Us = Us
        self.Ur = Ur
        self.ir_h_rep = self.ir_h_rep()

    def g_v_rep(self, include_ir_constraints=True):
        # The v-rep of G will be represented (s, vk_v_rep, pk_v_rep)
        g_v_rep = []
        for s in self.S:
            # Function to generate all non-empty subsets as indices
            def non_empty_index_subsets(n):
                return chain.from_iterable(combinations(range(n), r) for r in range(1, n+1))
            # Cartesian product of non-empty subsets' indices
            PA_T_indices = product(non_empty_index_subsets(len(self.T)),
                                   non_empty_index_subsets(len(self.A)))
            for Tt, At in PA_T_indices:
                pk_v_rep = self.pk_v_rep(s, Tt, At)
                vk_h_rep = self.vk_h_rep(s, Tt, At, include_ir_constraints=include_ir_constraints)
                vk_v_rep = h_rep_to_v_rep(vk_h_rep[0], vk_h_rep[1])
                if len(pk_v_rep[0]) > 0 and \
                   (len(vk_v_rep[0]) > 0 or len(vk_v_rep[1]) > 0 or len(vk_v_rep[2]) > 0):
                    g_v_rep.append((s, vk_v_rep, pk_v_rep))
        return g_v_rep

    # mieux vaut memoiser et faire les technique du 2 a 2
    def BNE_v_rep(self):
        # The v-rep of BNE will be represented (vk_v_rep, pk_v_rep)
        BNE_v_rep = []
        K = self.non_empty_k_in_g(include_ir_constraints=True)
        print("size of K: " + str(len(K)))

        # The case len(Kt) == 1
        for k in K:
            s, Tt, At = k
            pk_v_rep = self.pk_v_rep(s, Tt, At)
            vk_h_rep = self.vk_h_rep(s, Tt, At, include_ir_constraints=True)
            vk_v_rep = h_rep_to_v_rep(vk_h_rep[0], vk_h_rep[1])
            BNE_v_rep.append((vk_v_rep, pk_v_rep))

        # The case len(Kt) == 2 and construction of the graph
        for k1 in range(len(K)):
            for k2 in range(len(K)):
                if k1 != k2:
                    Kt = [K[k1], K[k2]]
                    vKt_v_rep = self.vKt_v_rep(Kt, include_ir_constraints=True)
                    Pjoin_v_rep = self.Pjoin_v_rep(Kt)
                    if len(vKt_v_rep[0]) > 0:
                        BNE_v_rep.append((vKt_v_rep, Pjoin_v_rep))
                        # construir le graph

        print("size of BNE: " + str(len(BNE_v_rep)))
        return BNE_v_rep

    def ir_h_rep(self):
        ir_ineq = []
        ir_eq = []
        for s in self.S:
            irs_ineq, irs_eq = self.__irs_h_rep(s)
            ir_ineq.extend(irs_ineq)
            ir_eq.extend(irs_eq)
        return canonicalize_h_rep(ir_ineq, ir_eq)

    @memoize_lists
    def vk_h_rep(self, s, Tt, At, include_ir_constraints=True):
        vk_ineq, vk_eq = self.__vk_h_rep(s, Tt, At)
        if include_ir_constraints:
            vk_ineq.extend(self.ir_h_rep[0])
            vk_eq.extend(self.ir_h_rep[1])
        return canonicalize_h_rep(vk_ineq, vk_eq)

    @memoize_lists
    def pk_v_rep(self, s, Tt, At):
        ineq, eq = self.__pk_h_rep(s, Tt, At)
        return h_rep_to_v_rep(ineq, eq)

    def non_empty_k_in_g(self, include_ir_constraints=True):
        K = []
        for s in self.S:
            # Function to generate all non-empty subsets as indices
            def non_empty_index_subsets(n):
                return chain.from_iterable(combinations(range(n), r) for r in range(1, n+1))
            # Cartesian product of non-empty subsets' indices
            PA_T_indices = product(non_empty_index_subsets(len(self.T)),
                                   non_empty_index_subsets(len(self.A)))
            for Tt, At in PA_T_indices:
                pk_v_rep = self.pk_v_rep(s, Tt, At)
                vk_h_rep = self.vk_h_rep(s, Tt, At, include_ir_constraints=include_ir_constraints)
                vk_v_rep = h_rep_to_v_rep(vk_h_rep[0], vk_h_rep[1])
                if len(pk_v_rep[0]) > 0 and \
                   (len(vk_v_rep[0]) > 0 or len(vk_v_rep[1]) > 0 or len(vk_v_rep[2]) > 0):
                    K.append((s, Tt, At))
        return K

    # vaut le coup de faire une version memoiser pour economiser du calcule
    def vKt_v_rep(self, Kt, include_ir_constraints=True):
        # Kt is a set of (s, Tt, AT)
        ineq_vKt, eq_vKt = [], []
        for k in Kt:
            vk_ineq, vk_eq = self.vk_h_rep(k[0], k[1], k[2],
                                           include_ir_constraints=include_ir_constraints)
            ineq_vKt.extend(vk_ineq)
            eq_vKt.extend(vk_eq)
        return h_rep_to_v_rep(ineq_vKt, eq_vKt)

    def Pjoin_v_rep(self, Kt):
        # Kt is a set of (s, Tt, AT)
        V = []
        for k in Kt:
            V.extend(self.pk_v_rep(k[0], k[1], k[2])[0])
        return canonicalize_v_rep(V, [], [])

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

    def __vk_h_rep(self, s, Tt, At, include_ir_constraints=True):
        # We define the H-rep of VY to get his V-rep for the vec (vt1, ..., vtn, y(a1), ..., y(an))
        # [There is a better methode]
        ineq_vy = []
        eq_vy = []
        lT = len(self.T)
        lA = len(self.A)
        # 0 <= y(ai) for ai in At
        for i in At:
            ineq = np.zeros(1 + lT + lA)
            ineq[1 + lT + i] = 1
            ineq_vy.append(ineq)
        # 0 = y(ai) for ai not in At
        for i in range(lA):
            if i not in At:
                eq = np.zeros(1 + lT + lA)
                eq[1 + lT + i] = 1
                eq_vy.append(eq)
        # 0 = -1 + sum_i y(ai)
        eq = np.zeros(1 + lT + lA)
        eq[0] = -1
        for i in range(lA):
            eq[1 + lT + i] = 1
        eq_vy.append(eq)
        # 0 = vt - sum_i y(ai)Us(t,s,ai) for t in Tt
        for i in Tt:
            eq = np.zeros(1 + lT + lA)
            eq[1 + i] = 1
            for ia in range(lA):
                eq[1 + lT + ia] = -self.Us_index(i, s, ia, s_index=False)
            eq_vy.append(eq)
        # 0 <= vt + sum_i y(ai)Us(t,s,ai) for i not in Tt
        for i in range(lT):
            if i not in Tt:
                ineq = np.zeros(1 + lT + lA)
                ineq[1 + i] = 1
                for ia in range(lA):
                    ineq[1 + lT + ia] = -self.Us_index(i, s, ia, s_index=False)
                ineq_vy.append(ineq)

        # Get the V-rep of VY
        V, R, L = h_rep_to_v_rep(ineq_vy, eq_vy)

        # Get the V-rep of vk
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
