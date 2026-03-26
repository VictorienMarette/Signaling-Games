import numpy as np
import cdd


# Convention H-rep: liste de [b, a1, a2....] (0 <= b +a1*x1+...) and a liste of eq [b, a1, a2....]
#            V-rep: set of V(conv hull), a set of R(cone) and a set L(vec space)


def h_rep_to_v_rep(ineq, eq):
    lin_set = set(list(range(len(eq))))
    mat = cdd.matrix_from_array(eq+ineq, rep_type=cdd.RepType.INEQUALITY, lin_set=lin_set)
    poly = cdd.polyhedron_from_matrix(mat)
    ext = cdd.copy_generators(poly)
    points = ext.array
    V = [v[1:] for v in points if v[0] == 1]
    R = [points[i][1:] for i in range(len(points)) if points[i][0] == 0 and i not in ext.lin_set]
    L = [points[i][1:] for i in range(len(points)) if points[i][0] == 0 and i in ext.lin_set]
    return V, R, L


def v_rep_to_h_rep(V, R, L):
    V2 = [np.insert(v, 0, 1) for v in V]
    R2 = [np.insert(r, 0, 0) for r in R]
    L2 = [np.insert(le, 0, 0) for le in L]
    lin_set = list(range(len(L2)))
    mat = cdd.matrix_from_array(L2+R2+V2, rep_type=cdd.RepType.GENERATOR, lin_set=lin_set)
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


def canonicalize_v_rep(V, R, L):
    V2 = [np.insert(v, 0, 1) for v in V]
    R2 = [np.insert(r, 0, 0) for r in R]
    L2 = [np.insert(le, 0, 0) for le in L]
    lin_set = list(range(len(L2)))
    mat = cdd.matrix_from_array(L2+R2+V2, rep_type=cdd.RepType.GENERATOR, lin_set=lin_set)
    i_non_red = cdd.matrix_canonicalize(mat)[2]
    points = mat.array
    V = [points[i][1:] for i in range(len(points))
         if i_non_red[i] is not None and points[i][0] == 1]
    R = [points[i][1:] for i in range(len(points))
         if i_non_red[i] is not None and points[i][0] == 0 and i not in mat.lin_set]
    L = [points[i][1:] for i in range(len(points))
         if i_non_red[i] is not None and points[i][0] == 0 and i in mat.lin_set]
    return V, R, L
