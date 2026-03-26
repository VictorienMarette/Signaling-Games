import numpy as np
import cdd


# Convention V-rep: set of V and set of R
#            H-rep: liste de [b, a1, a2....] (0 <= b +a1*x1+...) and a liste of eq [b, a1, a2....]


def h_rep_to_v_rep(ineq, eq):
    lin_set = set(list(range(len(eq))))
    mat = cdd.matrix_from_array(eq+ineq, rep_type=cdd.RepType.INEQUALITY, lin_set=lin_set)
    poly = cdd.polyhedron_from_matrix(mat)
    ext = cdd.copy_generators(poly)
    return [v[1:] for v in ext.array if v[0] == 1], [v[1:] for v in ext.array if v[0] == 0]


def v_rep_to_h_rep(V, R):
    V2 = [np.insert(v, 0, 1) for v in V]
    R2 = [np.insert(r, 0, 0) for r in R]
    mat = cdd.matrix_from_array(R2+V2, rep_type=cdd.RepType.GENERATOR)
    poly = cdd.polyhedron_from_matrix(mat)
    ext = cdd.copy_inequalities(poly)
    ineq = [ineq for i, ineq in enumerate(ext.array) if i not in ext.lin_set]
    eq = [ext.array[i] for i in ext.lin_set]
    return ineq, eq


def canonicalize_h_rep(ineq, eq):
    lin_set = set(list(range(len(eq))))
    mat = cdd.matrix_from_array(eq+ineq, rep_type=cdd.RepType.INEQUALITY, lin_set=lin_set)
    index_non_redundancies = cdd.matrix_canonicalize(mat)[2]
    ineq = [mat.array[i] for i in index_non_redundancies if i not in mat.lin_set and i is not None]
    eq = [mat.array[i] for i in index_non_redundancies if i in mat.lin_set and i is not None]
    return ineq, eq


def canonicalize_v_rep(V, R):
    V2 = [np.insert(v, 0, 1) for v in V]
    R2 = [np.insert(r, 0, 0) for r in R]
    mat = cdd.matrix_from_array(R2+V2, rep_type=cdd.RepType.GENERATOR)
    index_non_redundancies = cdd.matrix_canonicalize(mat)[2]
    ext = [mat.array[i] for i in index_non_redundancies if i is not None]
    return [v[1:] for v in ext if v[0] == 1], [v[1:] for v in ext if v[0] == 0]
