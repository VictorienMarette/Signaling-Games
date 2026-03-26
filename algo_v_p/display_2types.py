from scipy.spatial import ConvexHull
import plotly.graph_objects as go
import numpy as np

from polyhedrons import h_rep_to_v_rep, v_rep_to_h_rep, canonicalize_v_rep


colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']
color_irs = 'gray'


def display_2types_g(SignalingGame, min_v, max_v,
                     title="Representation of G",
                     ir_constrained=False, display_ir=False,
                     display=True, save_html_file_name=None):

    G = SignalingGame.g_v_rep(include_ir_constraints=ir_constrained)

    legend_names = SignalingGame.S

    fig = go.Figure()

    for g in G:
        # get g in the right format
        vertices = []
        pk_v_rep = g[2]
        V, R, L = g[1]
        vk_v_rep = boxed_vk_v_rep(V, R, L, min_v, max_v)

        for v_p in pk_v_rep[0]:
            for v_v in vk_v_rep[0]:
                vertices.append([v_v[0], v_p[0], v_v[1]])

        color = colors[SignalingGame.S.index(g[0])]

        add_trace_convexhull(vertices, fig, color)

    # Add static 2D legend
    for name, color in zip(legend_names, colors):
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            mode="markers",
            marker=dict(size=18, color=color),
            name=name
        ))

    if display_ir:
        vertices = []
        ineq, eq = SignalingGame.ir_h_rep
        ineq, eq = boxed_vk_h_rep(ineq, eq, min_v, max_v)
        V, R, L = h_rep_to_v_rep(ineq, eq)
        for v in V:
            vertices.append([v[0], 0, v[1]])
            vertices.append([v[0], 1, v[1]])
        print(vertices)
        add_trace_convexhull(vertices, fig, color_irs)
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            mode="markers",
            marker=dict(size=18, color=color_irs),
            name="IR"
        ))

    # Layout
    fig.update_layout(
                    scene=dict(
                        xaxis_title='V_'+SignalingGame.T[0],
                        yaxis_title='p('+SignalingGame.T[0]+")",
                        zaxis_title='V_'+SignalingGame.T[1],
                        xaxis=dict(range=[min_v, max_v]),
                        yaxis=dict(range=[0, 1]),
                        zaxis=dict(range=[min_v, max_v]),
                        aspectmode='manual',
                        aspectratio=dict(
                            x=1,
                            y=3/4,
                            z=1
                        ),
                        camera=dict(
                                    projection=dict(
                                        type='orthographic'
                                    )
                        )
                    ),
                    title=title
                )

    if display:
        fig.show()

    if save_html_file_name is not None:
        fig.write_html(save_html_file_name)


def display_2types_BNE(SignalingGame, min_v, max_v,
                       title="Representation of BNE",
                       display_ir=False, color="blue",
                       display=True, save_html_file_name=None):

    BNE = SignalingGame.BNE_v_rep()

    fig = go.Figure()

    for bne in BNE:
        # get bne in the right format
        vertices = []
        pk_v_rep = bne[1]
        V, R, L = bne[0]
        vk_v_rep = boxed_vk_v_rep(V, R, L, min_v, max_v)

        for v_p in pk_v_rep[0]:
            for v_v in vk_v_rep[0]:
                vertices.append([v_v[0], v_p[0], v_v[1]])

        add_trace_convexhull(vertices, fig, color)

    if display_ir:
        vertices = []
        ineq, eq = SignalingGame.ir_h_rep
        ineq, eq = boxed_vk_h_rep(ineq, eq, min_v, max_v)
        V, R, L = h_rep_to_v_rep(ineq, eq)
        for v in V:
            vertices.append([v[0], 0, v[1]])
            vertices.append([v[0], 1, v[1]])
        print(vertices)
        add_trace_convexhull(vertices, fig, color_irs)
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            mode="markers",
            marker=dict(size=18, color=color_irs),
            name="IR"
        ))

    # Layout
    fig.update_layout(
                    scene=dict(
                        xaxis_title='V_'+SignalingGame.T[0],
                        yaxis_title='p('+SignalingGame.T[0]+")",
                        zaxis_title='V_'+SignalingGame.T[1],
                        xaxis=dict(range=[min_v, max_v]),
                        yaxis=dict(range=[0, 1]),
                        zaxis=dict(range=[min_v, max_v]),
                        aspectmode='manual',
                        aspectratio=dict(
                            x=1,
                            y=3/4,
                            z=1
                        ),
                        camera=dict(
                                    projection=dict(
                                        type='orthographic'
                                    )
                        )
                    ),
                    title=title
                )

    if display:
        fig.show()

    if save_html_file_name is not None:
        fig.write_html(save_html_file_name)


def boxed_vk_h_rep(ineq, eq, min_v, max_v):
    ineq.append([-min_v, 1, 0])
    ineq.append([-min_v, 0, 1])
    ineq.append([max_v, -1, 0])
    ineq.append([max_v, 0, -1])
    return ineq, eq


def boxed_vk_v_rep(V, R, L, min_v, max_v):
    ineq, eq = v_rep_to_h_rep(V, R, L)
    ineq.append([-min_v, 1, 0])
    ineq.append([-min_v, 0, 1])
    ineq.append([max_v, -1, 0])
    ineq.append([max_v, 0, -1])
    return h_rep_to_v_rep(ineq, eq)


def add_trace_convexhull(vertices, fig, color="blue", name="Object"):
    if len(vertices) == 0:
        return
    vertices, _, _ = canonicalize_v_rep(vertices, [], [])
    vertices = np.asarray(vertices)
    points = np.array(vertices)
    dim = np.linalg.matrix_rank(points - points[0])

    if dim == 0:
        # Single point
        fig.add_trace(go.Scatter3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            mode='markers',
            marker=dict(size=3, color=color),
            showlegend=False,
            name=name
        ))

    elif dim == 1:
        fig.add_trace(go.Scatter3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            mode='lines+markers',
            line=dict(color=color, width=5),
            marker=dict(size=3, color=color),
            showlegend=False,
            name=name
        ))

    elif dim == 2:
        def normal_vec(A, B, C):
            A, B, C = np.array(A), np.array(B), np.array(C)
            normal = np.cross(B - A, C - A)
            normal /= np.linalg.norm(normal)
            return normal
        epsi = 0.01
        normal = normal_vec(vertices[0], vertices[1], vertices[2])
        vertices2 = np.empty((0, 3))
        for v in vertices:
            vertices2 = np.vstack([vertices2, v + epsi*normal])
        vertices = np.vstack([vertices, vertices2])

        hull = ConvexHull(vertices)
        fig.add_trace(go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=hull.simplices[:, 0],
            j=hull.simplices[:, 1],
            k=hull.simplices[:, 2],
            opacity=0.5,
            color=color,
            showlegend=False,
            name=name
        ))

    elif dim == 3:
        # 3D convex hull
        hull = ConvexHull(vertices)
        fig.add_trace(go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=hull.simplices[:, 0],
            j=hull.simplices[:, 1],
            k=hull.simplices[:, 2],
            opacity=0.5,
            color=color,
            showlegend=False,
            name=name
        ))
