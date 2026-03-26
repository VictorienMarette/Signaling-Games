from SignalingGame import SignalingGame
from display_2types import display_2types_g, add_trace_convexhull
from scipy.spatial import ConvexHull
import plotly.graph_objects as go
import numpy as np


T = ["W", "S"]
S = ["B", "Q"]
A = ["F", "C"]


def Us(t, s, a):
    tot = 0
    if a == "C":
        tot += 2
    if (t == "W" and s == "Q") or (t == "S" and s == "B"):
        tot += 1
    return tot


def Ur(t, s, a):
    if (t == "W" and a == "F") or (t == "S" and a == "C"):
        return 1
    return 0


"""
G = SignalingGame(T, S, A, Us, Ur)
display_2types_g(G, 0, 4, ir_constrained=False, display_ir=True)
"""

fig = go.Figure()
add_trace_convexhull([[0, 0, 1], [0,1,0], [0.5,0.5,0], [0.7,0.2,0.1]], fig, color="blue", name="Object")
# Layout
fig.update_layout(
                scene=dict(
                    xaxis_title='V_',
                    yaxis_title='p(',
                    zaxis_title='V_',
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
                )
            )
fig.show()