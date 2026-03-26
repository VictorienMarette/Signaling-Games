from scipy.spatial import ConvexHull
import plotly.graph_objects as go
import numpy as np

from polyhedrons import h_rep_to_v_rep, v_rep_to_h_rep


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


def boxed_vk_v_rep(V, R, L, min_v, max_v):
    ineq, eq = v_rep_to_h_rep(V, R, L)
    ineq.append([-min_v, 1, 0])
    ineq.append([-min_v, 0, 1])
    ineq.append([max_v, -1, 0])
    ineq.append([max_v, 0, -1])
    return h_rep_to_v_rep(ineq, eq)


def add_trace_convexhull(vertices, fig, color="blue", name=None):
    vertices = np.asarray(vertices)
    n = len(vertices)

    # Optionnel : nom par défaut
    if name is None:
        name = "Object"

    if n == 1:
        # Point
        fig.add_trace(go.Scatter3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            mode='markers',
            marker=dict(size=5, color=color),
            showlegend=False,
            name=name
        ))

    elif n == 2:
        # Segment
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

    elif n >= 3:
        try:
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

        except Exception:
            pass
