from plotly import graph_objs as go
import numpy as np
from dash import html
import dash_bootstrap_components as dbc


def generate_macd_plot(df, base, target, bg_color="white", opacity=0.3):

    # Creating MACD Chart
    figure_trend = go.Figure()

    line_MACD = go.Scatter(
        x=df["Date"],
        y=df["MACD"],
        mode="lines",
        line=dict(color="green"),
        name="MACD",
    )

    line_MACD_Signal = go.Scatter(
        x=df["Date"],
        y=df["MACD_Signal"],
        mode="lines",
        line=dict(color="red"),
        name="MACD_Signal",
    )

    df["MACD_bar"] = df["MACD"] - df["MACD_Signal"]

    # Setting color for the MACD bar
    y = np.array(df["MACD_bar"])
    color = np.array(["rgb(255,255,255)"] * y.shape[0])
    color[y < 0] = "firebrick"
    color[y >= 0] = "green"

    bar_MACD = go.Bar(
        x=df["Date"],
        y=df["MACD_bar"],
        marker=dict(color=color.tolist()),
        opacity=opacity,
    )

    figure_trend.add_trace(line_MACD)
    figure_trend.add_trace(line_MACD_Signal)
    figure_trend.add_trace(bar_MACD)

    figure_trend.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["close"],
            mode="lines",
            yaxis="y99",
            name="price",
            line=dict(color="lightgray"),
        )
    )

    figure_trend.update_layout(
        **{
            "yaxis99": dict(
                overlaying="y",
                showticklabels=True,
                side="right",
                title="price",
                color="lightgray",
            )
        }
    )
    figure_trend.update_xaxes(
        showspikes=True,
        spikecolor="gray",
        spikesnap="cursor",
        spikemode="across",
        spikethickness=1,
    )

    figure_trend.update_yaxes(
        showspikes=True,
        spikecolor="gray",
        spikesnap="cursor",
        spikemode="across",
        spikethickness=1,
    )

    figure_trend.update_layout(
        barmode="relative",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
        ),
        plot_bgcolor=bg_color,
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="#F3f3f3",
            showticklabels=True,
        ),
        margin={"b": 0, "t": 0},
        showlegend=False,
        hovermode="x unified",
    )
    return figure_trend


def calculate_perc_vs_initial_date(df, col):
    """
    Calculates % difference against initial date for kpi calcs
    """
    return round(((df[col].iloc[-1] / df[col].iloc[0]) - 1) * 100, 1)


def calculate_perc_vs_previous_date(df, col):
    """
    Calculates % difference vs previous date for kpi calcs
    """
    return round(((df[col].iloc[-1] / df[col].iloc[-2]) - 1) * 100, 1)


def color_percent_change(pc):
    """
    Set green / red colors for kpi % changes
    """
    if pc > 0:
        return "green"
    else:
        return "red"


def create_percent_change_24h_div(pc, pc_color):
    """
    Create kpi div for last 24h percent change
    """
    return html.Div(
        [
            html.P(
                "Last 24h: ",
                style={"display": "inline"},
                className="kpi-historic-period",
            ),
            html.P(
                pc,
                style={
                    "color": pc_color,
                    "display": "inline",
                    "font-weight": "bold",
                },
            ),
        ],
    )


def create_percent_change_vs_initial_div(pc, pc_color, initial_date):
    """
    Create kpi div for initial date percent change
    """

    return html.Div(
        [
            html.P(
                "{}: ".format(initial_date),
                style={"display": "inline"},
                className="kpi-historic-period",
            ),
            html.P(
                pc,
                style={
                    "color": pc_color,
                    "display": "inline",
                    "font-weight": "bold",
                },
            ),
        ],
        className="kpi-historic-period-div",
    )


def monthdelta(date, month_delta):
    """
    Calculates day difference of month_delta
    """
    m, y = (
        (date.month + month_delta) % 12,
        date.year + ((date.month) + month_delta - 1) // 12,
    )
    if not m:
        m = 12
    d = min(
        date.day,
        [
            31,
            29 if y % 4 == 0 and (not y % 100 == 0 or y % 400 == 0) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ][m - 1],
    )
    date_prev = date.replace(day=d, month=m, year=y)
    difference = date - date_prev

    return difference.days


def create_tooltip(id, tooltip_text):
    return html.Div(
        children=[
            html.Span(
                "?",
                id=id,
                style={"textAlign": "center", "color": "white",},
                className="dot",
            ),
            dbc.Tooltip(tooltip_text, target=id, autohide=False),
        ],
        style={"display": "inline"},
    )


def create_tooltip_row(id, tooltip_text, label):
    dbc_row = dbc.Row(
        [
            html.P(label, className="tooltip-text"),
            create_tooltip(id, tooltip_text),
        ],
        className="tooltip-row-top",
    )
    return dbc_row


def print_info(text, printer=True):
    if printer:
        print("[INFO]: Triggered by {}".format(text))
