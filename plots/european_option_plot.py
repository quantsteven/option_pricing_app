import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.constants import *
from utils.registry import get_price, get_payoff, get_greeks


def plot_price(
    model: str, instrument: str, method: str, param: dict, anchor: str = "S", vlines: list[str] = ["K"]
) -> go.Figure:
    spot = param[anchor]
    """Plot Option Premium vs Spot Price"""
    underlying_vec = np.linspace(LB * spot, UB * spot, NUM_OF_PT)
    payoff_vec, premium_vec = [], []
    for Si in underlying_vec:
        param_i = {**param, anchor: Si}
        payoff_vec.append(get_payoff(instrument=instrument, param=param_i))
        premium_vec.append(get_price(model=model, instrument=instrument, method=method, param=param_i))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=underlying_vec, y=payoff_vec, mode="markers+lines", name="Payoff", line=dict(color=PURPLE))
    )
    fig.add_trace(
        go.Scatter(x=underlying_vec, y=premium_vec, mode="markers+lines", name="Premium", line=dict(color=CYAN))
    )

    for v in vlines:
        fig.add_vline(x=param[v], line_dash="dash", line_color=SHAN_HU_FEN, annotation_text=v)

    fig.update_layout(
        title=f"{param['option_type'].capitalize()} Payoff | Premium vs Spot"
              f"\n(Current Spot = {spot})",
        showlegend=True,
        xaxis_title="Underlying",
        yaxis_title="Value",
        title_font_color=JING,
        height=400,
        width=1200
    )

    return fig


def plot_greeks(
    model: str, instrument: str, method: str, param: dict, selected: list[str],
    anchor: str = "S", vlines: list[str] = ["K"]
) -> go.Figure:
    spot = param[anchor]
    underlying_vec = np.linspace(LB * spot, UB * spot, NUM_OF_PT)

    greek_res = []
    for Si in underlying_vec:
        param_i = {**param, anchor: Si}
        greek_res.append(
            get_greeks(model=model, instrument=instrument, method=method, param=param_i, selected=selected)
        )

    l = len(greek_res[0])
    num_rows = l * len(selected)

    if l == 1:
        fig = make_subplots(
            rows=num_rows, cols=1, shared_xaxes=False, vertical_spacing=0.05,
            subplot_titles=[f"{greek.title()} (Numerical)" for greek in selected]
        )
    else:
        fig = make_subplots(
            rows=num_rows, cols=1, shared_xaxes=False, vertical_spacing=0.03,
            subplot_titles=[
                f"{greek.title()} (Analytical vs Numerical)" if i % 2 == 0 else f"{greek.title()} (Spread)"
                for greek in selected for i in range(2)
            ]
        )

    for i, greek in enumerate(selected):
        if l == 1:
            greek_num_vec = [res["Numerical"][greek] for res in greek_res]
            fig.add_trace(
                go.Scatter(x=underlying_vec, y=greek_num_vec, mode="markers+lines", name=f"{greek.title()} Numerical"),
                row=i+1, col=1
            )
            for v in vlines:
                fig.add_vline(x=param[v], line_dash="dash", line_color=SHAN_HU_FEN, row=i+1, col=1, annotation_text=v)
            fig.update_xaxes(title_text="Underlying", row=i+1, col=1)
            fig.update_yaxes(title_text="Value", row=i+1, col=1)

        else:
            greek_ana_vec = [res["Analytical"][greek] for res in greek_res]
            greek_num_vec = [res["Numerical"][greek] for res in greek_res]
            greek_spread_vec = [a - n for a, n in zip(greek_ana_vec, greek_num_vec)]

            row_value = 2 * i + 1
            row_spread = 2 * i + 2

            fig.add_trace(
                go.Scatter(x=underlying_vec, y=greek_ana_vec, mode="markers+lines", name=f"{greek.title()} Analytical"),
                row=row_value, col=1
            )
            fig.add_trace(
                go.Scatter(x=underlying_vec, y=greek_num_vec, mode="markers+lines", name=f"{greek.title()} Numerical"),
                row=row_value, col=1
            )

            # Plot spread
            fig.add_trace(
                go.Scatter(
                    x=underlying_vec, y=greek_spread_vec,
                    fill='tonexty',  # fill area between this and previous trace
                    fillcolor='rgba(0,100,80,0.2)',  # semi-transparent fill,
                    line=dict(color='rgb(0,100,80)'),
                    name=f"{greek.title()} Spread"
                ), row=row_spread, col=1
            )

            for v in vlines:
                x = param[v]
                fig.add_vline(x=x, line_dash="dash", line_color=SHAN_HU_FEN, row=row_value, col=1, annotation_text=v)
                fig.add_vline(x=x, line_dash="dash", line_color=SHAN_HU_FEN, row=row_spread, col=1, annotation_text=v)

            fig.update_xaxes(title_text="Underlying", row=row_spread, col=1)
            fig.update_yaxes(title_text="Value", row=row_value, col=1)
            fig.update_yaxes(title_text="Spread", row=row_spread, col=1)

    fig.update_layout(
        title=f"{param['option_type'].capitalize()} Greeks \n(Current Spot = {spot})",
        showlegend=True,
        title_font_color=JING,
        height=400 * num_rows,
        width=1200
    )

    return fig
