import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from app_functions import *
from datetime import datetime
from app_dropdown import *
import dash_daq as daq


# Start by displaying L3M
initial_limit = monthdelta(datetime.today(), -3)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
        },
        {
            "name": "description",
            "content": "Price. Trend. Capitalization. Coin Rank. Social Metrics. On Chain Metrics.",
        },
    ],
)
server = app.server

app.title = "Crypto Dash"

quick_selectors_div = html.Div(
    [
        dbc.ButtonGroup(
            [
                dbc.Button("1M", id="1M", color="primary", outline=True),
                dbc.Button(
                    "3M", id="3M", color="primary", outline=True, active=True
                ),
                dbc.Button("6M", id="6M", color="primary", outline=True),
                dbc.Button("1Y", id="1Y", color="primary", outline=True),
                dbc.Button("3Y", id="3Y", color="primary", outline=True),
                dbc.Button("ALL", id="ALL", color="primary", outline=True),
                dbc.Button(
                    "CUSTOM", id="CUSTOM", color="primary", outline=True
                ),
            ],
            className="quick-selector-buttons",
        ),
        html.P(
            id="output-button",
            className="output-buttons-text",
            style={"display": "none"},
        ),
    ],
    className="quick-selectors-div",
)

range_slider_div = dbc.Container(
    id="range-slider-div",
    className="range-slider-div",
    children=[
        dbc.Row(
            children=[
                # Represents all range
                html.P(id="range-min-max", style={"display": "none"}),
                # Represents quick selectors or submit range interval
                html.P(id="period-min-max", style={"display": "none"}),
                dbc.Col(
                    children=[
                        # Visible slider range
                        html.P(
                            id="range-min-max-date", className="text-center"
                        ),
                        dcc.RangeSlider(
                            id="my-range-slider",
                            min=0,
                            max=15,
                            step=1,
                            allowCross=False,
                            className="range-slider-style",
                        ),
                    ],
                    className="col-8",
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Apply",
                            id="submit-range-button",
                            color="primary",
                            outline=True,
                        )
                    ],
                    className="col-4",
                ),
            ],
        )
    ],
)


shared_selectors = dbc.Card(
    dbc.Row(
        children=[
            # Change to side-by-side for mobile layout
            dbc.Col(
                style={"display": "none"},
                className="div-for-dropdown",
                children=[
                    dcc.Dropdown(
                        id="resolution-dropdown",
                        value="day",
                        options=[
                            {"label": "hour", "value": "hour"},
                            {"label": "day", "value": "day"},
                        ],
                        placeholder="Select resolution",
                    )
                ],
            ),
            dbc.Col(
                className="div-for-dropdown col-9",
                children=[
                    # Dropdown to select times
                    dcc.Dropdown(
                        id="target-selector",
                        value="BTC",
                        # options=[
                        #     {"label": c, "value": c,} for c in crypto_list
                        # ],
                        options=crypto_dict,
                        placeholder="Select target currency",
                        searchable=True,
                    )
                ],
            ),
            # Activate When having multiple bases available
            dbc.Col(
                style={"display": "none"},
                className="div-for-dropdown",
                children=[
                    # Dropdown to select times
                    dcc.Dropdown(
                        id="base-selector",
                        value="USD",
                        options=[
                            {"label": c, "value": c}
                            for c in ["USD", "BTC", "ETH"]
                        ],
                        placeholder="Select base currency",
                    )
                ],
            ),
            dbc.Col(
                dbc.Button(
                    "Submit",
                    id="submit-button",
                    color="success",
                    outline=True,
                ),
                className="col-3",
            ),
        ],
    ),
    className="controls-shared",
)


kpi_price_card_content = dbc.Card(
    [
        dbc.CardHeader(
            children=[
                html.Div("Last Price", style={"display": "inline"}),
                create_tooltip(
                    id="price-kpi-tooltip",
                    tooltip_text="Provides last price, % change since last day and selected period beginning. Updates hourly",
                ),
            ],
            className="rounded-top",
        ),
        dbc.CardBody(
            [
                dbc.Row(
                    children=[
                        dbc.Col(
                            html.P(
                                "",
                                className="card-text",
                                id="card-last-price",
                            ),
                            className="col-12 col-xl-6",
                        ),
                        dbc.Col(
                            html.Div(
                                [""],
                                className="card-text",
                                id="card-last-price-percent",
                            ),
                            className="col-12 col-xl-6",
                        ),
                    ],
                    justify="between",
                    align="center",
                    className="price-card-row",
                )
            ],
        ),
    ],
    className="kpi-div",
)


# price kpi, and trend
trend_page = [
    # Row for kpi & other objects above graphs
    dbc.Row(
        [
            dbc.Col(
                kpi_price_card_content,
                className="first-page-col col-12 col-xl-6",
            )
        ],
    ),
    html.Div(
        className="page-graphs",
        children=[
            dbc.Card(
                [
                    dbc.Row(
                        create_tooltip(
                            id="trend-graph-tooltip",
                            tooltip_text=[
                                html.A(
                                    "MACD ",
                                    href="https://www.investopedia.com/terms/m/macd.asp",
                                    target="_blank",
                                ),
                                """ 12-26-9 signifies market trend. When green line is above red, market is 
                                            in uptrend and when red line is above green, market is in downtrend. 
                                            Crossover between green-red lines signal market trend changes.
                                            """,
                            ],
                        ),
                        justify="end",
                        className="row-custom",
                    ),
                    dcc.Loading(
                        id="loading-trend-graph",
                        type="default",
                        fullscreen=False,
                        children=[dcc.Graph(id="trend-graph")],
                    ),
                ],
                className="page-1-graph-card",
            ),
        ],
    ),
]


sidebar = html.Div(
    id="sidebar",
    children=[
        html.A(
            children=[
                html.Img(
                    src=app.get_asset_url("crypto-dash-logo.png"),
                    className="crypto-dash-logo",
                )
            ],
            href="/",
        ),
        html.Hr(className="app-name-line"),
        dbc.Nav(
            [
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url(
                                        "navigation/price.png"
                                    )
                                ),
                                width=2,
                            ),
                            dbc.Col("Price"),
                        ],
                        justify="start",
                        align="center",
                    ),
                    id="price-nav",
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url(
                                        "navigation/trend.png"
                                    )
                                ),
                                width=2,
                            ),
                            dbc.Col("Trend"),
                        ],
                        justify="start",
                        align="center",
                    ),
                    href="/page-1",
                    active="exact",
                ),
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url(
                                        "navigation/total-cap.png"
                                    )
                                ),
                                width=2,
                            ),
                            dbc.Col("Capitalization"),
                        ],
                        justify="start",
                        align="center",
                    ),
                    href="/page-2",
                    active="exact",
                ),
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url(
                                        "navigation/rank.png"
                                    )
                                ),
                                width=2,
                            ),
                            dbc.Col("Coin Rank"),
                        ],
                        justify="start",
                        align="center",
                    ),
                    href="/page-3",
                    active="exact",
                ),
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url(
                                        "navigation/social.png"
                                    )
                                ),
                                width=2,
                            ),
                            dbc.Col("Social Metrics"),
                        ],
                        justify="start",
                        align="center",
                    ),
                    href="/page-4",
                    active="exact",
                ),
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url(
                                        "navigation/onchain.png"
                                    )
                                ),
                                width=2,
                            ),
                            dbc.Col("On Chain Metrics"),
                        ],
                        justify="start",
                        align="center",
                    ),
                    href="/page-5",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar-style",
)


content = html.Div(id="page-content", children=[])


app.layout = html.Div(
    className="layout-enter",
    children=[
        dcc.Location(id="url"),
        sidebar,
        # Right side Content + Header
        html.Div(
            children=[
                # Wrapping header card in collapse to be able to show/hide
                dbc.Collapse(
                    id="header",
                    # Header - Logo, Title, shared selectors, quick selectors
                    children=dbc.Card(
                        children=[
                            dbc.Container(
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            children=[
                                                dbc.Row(
                                                    children=[
                                                        dbc.Col(
                                                            shared_selectors,
                                                            className="col-xl-4 col-12",
                                                        ),
                                                        dbc.Col(
                                                            range_slider_div,
                                                            className="col-xl-4 col-12",
                                                        ),
                                                        dbc.Col(
                                                            quick_selectors_div,
                                                            className="col-xl-4 col-12",
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ],
                                    justify="between",
                                    align="center",
                                ),
                                fluid=True,
                            )
                        ],
                        className="header-card border-0",
                    ),
                ),
                dbc.Container(content, className="content-style", fluid=True),
            ],
            className="right-side-card",
        ),
        html.Div(
            children=[
                html.P(
                    "© 2022 Crypto Dash. All rights reserved. Powered by CryptoCompare & CoinGecko API.",
                    className="P-special",
                ),
                html.P(
                    "All the information here is provided as information only and we take no responsibility for the correctness of the data. This site does not provide financial advice of any kind. Any use of the data is solely at your own risk.",
                    className="P-special",
                ),
            ],
            className="disclaimer-div",
        ),
        # Stashed components
        html.Div(
            children=[
                # df holds jsonified ohlc df
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    fullscreen=True,
                    children=[
                        html.Div(id="df-ohlc-stash", style={"display": "none"})
                    ],
                    className="loading-div",
                ),
                # df main holds current page corresponding df
                html.Div(id="df-main-stash", style={"display": "none"}),
                html.Div(id="nclick-holder", style={"display": "none"}),
                html.Div(
                    id="submit-range-nclick-holder", style={"display": "none"},
                ),
                dcc.Store(id="submit-clicks", storage_type="local"),
            ]
        ),
    ],
)


@app.callback(
    [
        Output("page-content", "children"),
        Output("sidebar", "style"),
        Output("header", "is_open"),
    ],
    [Input("url", "pathname")],
)
def render_page_content(pathname):

    page_message = html.H1(
        "Page not available in demo version", className="text-danger"
    )

    if pathname == "/":
        return [page_message, {}, True]
    elif pathname == "/page-1":
        return [trend_page, {}, True]
    elif pathname == "/page-2":
        return [page_message, {}, True]
    elif pathname == "/page-3":
        return [page_message, {}, True]
    elif pathname == "/page-4":
        return [page_message, {}, True]
    elif pathname == "/page-5":
        return [page_message, {}, True]
    else:
        # If the user tries to reach a different page, return a 404 message
        return [
            dbc.Jumbotron(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognised..."),
                ]
            ),
            {"display": "none"},
            {"display": "none"},
        ]


# Create and stash dfs upon submit / page change
@app.callback(
    [
        Output("df-ohlc-stash", "children"),
        # Data for the page being viewed
        Output("df-main-stash", "children"),
    ],
    inputs=[Input("submit-button", "n_clicks"), Input("url", "pathname")],
    state=[
        State("target-selector", "value"),
        State("base-selector", "value"),
        State("resolution-dropdown", "value"),
        State("df-ohlc-stash", "children"),
    ],
)
def generate_stash_dfs(
    n_clicks, pathname, target, base, res, df_ohlc_stash,
):
    triggered_by = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    # Triggered by new symbol request
    if triggered_by == "submit-button":

        # User viewing price or trend page
        if pathname == "/" or pathname == "/page-1":
            df_ohlc = pd.read_csv("data/btc_trend.csv")

            df_ohlc_json = df_ohlc.to_json(date_format="iso", orient="split")

            return [df_ohlc_json, df_ohlc_json]

    # Triggered by page navigation
    else:
        # User viewing price or trend page and stash is empty
        if (
            pathname == "/" or pathname == "/page-1"
        ) and df_ohlc_stash is None:

            df_ohlc = pd.read_csv("data/btc_trend.csv")
            df_ohlc_json = df_ohlc.to_json(date_format="iso", orient="split")

            return [
                df_ohlc_json,
                df_ohlc_json,
            ]

        # All stashes are full prevent update
        else:
            if pathname == "/" or pathname == "/page-1":
                return [
                    df_ohlc_stash,
                    # df_cap_stash,
                    # df_rank_stash,
                    # df_social_stash,
                    df_ohlc_stash,
                ]


# KPIs - price / trend page
@app.callback(
    [
        Output("card-last-price", "children"),
        Output("card-last-price-percent", "children"),
    ],
    inputs=[
        Input("df-ohlc-stash", "children"),
        Input("range-min-max", "children"),
    ],
    state=[State("base-selector", "value")],
)
def render_price_kpis(jsonified_df, slider_range, base):
    df = pd.read_json(jsonified_df, orient="split")

    if slider_range is not None:
        smin, smax = slider_range.split("|")
        smin = int(smin)
        smax = int(smax)
        df = df.loc[smin:smax, :]
    else:
        df = df.loc[len(df) - 1 - initial_limit : len(df) - 1].copy()

    if base == "BTC":
        base_symbol = "BTC"
        last_price = np.format_float_positional(df["close"].iloc[-1])
        last_cap = np.format_float_positional(df["Market_Cap"].iloc[-1])
        last_total_cap = np.format_float_positional(
            df["total_market_cap"].iloc[-1]
        )

    elif base == "USD":
        base_symbol = "$"
        if df["close"].iloc[-1] < 1:
            last_price = "{:.4f}".format(df["close"].iloc[-1])
        else:
            round_digits = 2
            last_price = "{:.2f}".format(df["close"].iloc[-1])

    elif base == "ETH":
        base_symbol = "ETH"
        last_price = np.format_float_positional(df["close"].iloc[-1])

    perc_24h = calculate_perc_vs_previous_date(df, "close")

    initial_date = pd.to_datetime(df.Date).dt.strftime("%b %d, %Y").iloc[0]

    perc_vs_initial_date = calculate_perc_vs_initial_date(df, "close")

    perc_24_color = color_percent_change(perc_24h)

    perc_24h = str(perc_24h) + "%"

    perc_vs_initial_date_color = color_percent_change(perc_vs_initial_date)

    perc_vs_initial_date = str(perc_vs_initial_date) + "%"

    return [
        "{} {}".format(base_symbol, last_price),
        html.H6(
            [
                create_percent_change_24h_div(perc_24h, perc_24_color),
                create_percent_change_vs_initial_div(
                    perc_vs_initial_date,
                    perc_vs_initial_date_color,
                    initial_date,
                ),
            ]
        ),
    ]


# Activate the clicked quick selection button
@app.callback(
    [
        Output("output-button", "children"),
        Output("1M", "active"),
        Output("3M", "active"),
        Output("6M", "active"),
        Output("1Y", "active"),
        Output("3Y", "active"),
        Output("ALL", "active"),
        Output("CUSTOM", "active"),
    ],
    [
        Input("1M", "n_clicks"),
        Input("3M", "n_clicks"),
        Input("6M", "n_clicks"),
        Input("1Y", "n_clicks"),
        Input("3Y", "n_clicks"),
        Input("ALL", "n_clicks"),
        Input("CUSTOM", "n_clicks"),
        Input("submit-button", "n_clicks"),
    ],
)
def toggle_buttons(
    oneM, threeM, sixM, oneY, threeY, ALL, CUSTOM, submit_n_clicks
):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if not any(
        [oneM, threeM, sixM, oneY, threeY, ALL, CUSTOM, submit_n_clicks]
    ):
        return (
            "Nothing selected yet",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        )
    elif button_id == "1M":
        return (
            "1M is currently selected",
            True,
            False,
            False,
            False,
            False,
            False,
            False,
        )
    elif button_id == "3M" or button_id == "submit-button":
        return "3M is selected", False, True, False, False, False, False, False
    elif button_id == "6M":
        return "6M is selected", False, False, True, False, False, False, False
    elif button_id == "1Y":
        return "1Y is selected", False, False, False, True, False, False, False
    elif button_id == "3Y":
        return (
            "3Y is selected",
            False,
            False,
            False,
            False,
            True,
            False,
            False,
        )
    elif button_id == "ALL":
        return (
            "ALL is selected",
            False,
            False,
            False,
            False,
            False,
            True,
            False,
        )
    elif button_id == "CUSTOM":
        return (
            "CUSTOM is selected",
            False,
            False,
            False,
            False,
            False,
            False,
            True,
        )


# Hide / Show date range selector via CUSTOM button
@app.callback(
    [Output("range-slider-div", "style")],
    [
        Input("1M", "n_clicks"),
        Input("3M", "n_clicks"),
        Input("6M", "n_clicks"),
        Input("1Y", "n_clicks"),
        Input("3Y", "n_clicks"),
        Input("ALL", "n_clicks"),
        Input("CUSTOM", "n_clicks"),
    ],
)
def show_hide_date_slider(oneM, threeM, sixM, oneY, threeY, ALL, CUSTOM):

    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # print("slider update triggered by ", button_id)
    if button_id == "CUSTOM":
        return [{}]
    else:
        return [{"display": "none"}]


# Save slider updated values and update ranges
@app.callback(
    [
        Output("range-min-max", "children"),
        Output("period-min-max", "children"),
        Output("range-min-max-date", "children"),
        Output("submit-range-nclick-holder", "children"),
        Output("my-range-slider", "max"),
        Output("my-range-slider", "min"),
        Output("my-range-slider", "value"),
    ],
    inputs=[
        Input("df-main-stash", "children"),
        Input("submit-range-button", "n_clicks"),
        Input("1M", "n_clicks"),
        Input("3M", "n_clicks"),
        Input("6M", "n_clicks"),
        Input("1Y", "n_clicks"),
        Input("3Y", "n_clicks"),
        Input("ALL", "n_clicks"),
    ],
    state=[
        State("my-range-slider", "value"),
        State("submit-range-nclick-holder", "children"),
        State("period-min-max", "children"),
        State("1M", "active"),
        State("6M", "active"),
        State("1Y", "active"),
        State("3Y", "active"),
        State("ALL", "active"),
        State("CUSTOM", "active"),
    ],
)
def slider_send_update(
    # n_clicks,
    jsonified_df,
    submit_range_clicks,
    oneM,
    threeM,
    sixM,
    oneY,
    threeY,
    ALL,
    range_slider_value,
    # jsonified_df,
    previous_submit_range_clicks,
    period_min_max,
    M1_selector_active,
    M6_selector_active,
    Y1_selector_active,
    Y3_selector_active,
    ALL_selector_active,
    CUSTOM_selector_active,
):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        # print("slider update triggered by ", button_id)

    quick_selector_list = [
        M1_selector_active,
        M6_selector_active,
        Y1_selector_active,
        Y3_selector_active,
        ALL_selector_active,
        CUSTOM_selector_active,
    ]
    is_any_quick_selector_active = any(quick_selector_list)

    # Opening
    if button_id == "df-main-stash" and not is_any_quick_selector_active:
        df = pd.read_json(jsonified_df, orient="split")

        max_limit = len(df) - 1
        if max_limit - initial_limit > 0:
            min_limit = max_limit - initial_limit
        else:
            min_limit = 0

        date_end = df.loc[len(df) - 1, "Date"].strftime("%b %d, %Y")
        date_start = df.loc[len(df) - 1 - initial_limit, "Date"].strftime(
            "%b %d, %Y"
        )
        date_string = str(date_start) + " - " + str(date_end)

        return [
            str(min_limit) + "|" + str(max_limit),
            None,
            date_string,
            submit_range_clicks,
            max_limit,
            min_limit,
            [min_limit, max_limit],
        ]

    elif button_id == "submit-range-button" or CUSTOM_selector_active:
        df = pd.read_json(jsonified_df, orient="split")
        is_daily = int(pd.to_datetime(df.Date).dt.strftime("%H").sum()) == 0
        if is_daily:
            date_start = pd.to_datetime(df.Date).dt.strftime("%b %d, %Y")[
                range_slider_value[0]
            ]
            date_end = pd.to_datetime(df.Date).dt.strftime("%b %d, %Y")[
                range_slider_value[1]
            ]
            date_string = str(date_start) + " - " + str(date_end)
        else:
            date_start = pd.to_datetime(df.Date).dt.strftime("%b %d, %H:%M")[
                range_slider_value[0]
            ]
            date_end = pd.to_datetime(df.Date).dt.strftime("%b %d, %H:%M")[
                range_slider_value[1]
            ]
            date_string = str(date_start) + " - " + str(date_end)

        # for opening
        if period_min_max is None:
            range_max = initial_limit
            range_min = 0
        # retrieve from buttons
        else:
            range_min, range_max = period_min_max.split("|")

        return [
            str(range_slider_value[0]) + "|" + str(range_slider_value[1]),
            period_min_max,
            date_string,
            submit_range_clicks,
            int(range_max),
            int(range_min),
            [range_slider_value[0], range_slider_value[1]],
        ]
    # Triggered by quick period selectors
    else:
        df = pd.read_json(jsonified_df, orient="split")
        if button_id == "1M":
            period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -1)

        elif button_id == "3M":
            period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -3)

        elif button_id == "6M":
            period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -6)

        elif button_id == "1Y":
            period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -12)

        elif button_id == "3Y":
            period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -36)

        elif button_id == "ALL":
            period_look_back = 9999999

        period_max = len(df) - 1
        print("button id = ", button_id)

        # Find out active button
        if button_id == "df-main-stash":
            # Get which selector is active
            true_idx = [i for i, x in enumerate(quick_selector_list) if x][0]
            if true_idx == 0:
                period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -1)

            elif true_idx == 1:
                period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -6)

            elif true_idx == 2:
                period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -12)

            elif true_idx == 3:
                period_look_back = monthdelta(df.loc[len(df) - 1, "Date"], -36)

            elif true_idx == 4:
                period_look_back = 9999999

        if period_look_back <= period_max:
            period_min = period_max - period_look_back
        else:
            period_min = 0

        date_start = df.loc[period_min, "Date"].strftime("%b %d, %Y")

        date_end = df.loc[period_max, "Date"].strftime("%b %d, %Y")

        date_string = str(date_start) + " - " + str(date_end)

        return [
            str(period_min) + "|" + str(period_max),
            str(period_min) + "|" + str(period_max),
            date_string,
            submit_range_clicks,
            int(period_max),
            int(period_min),
            [int(period_min), int(period_max)],
        ]


# Generate trend plot (MACD)
@app.callback(
    Output("trend-graph", "figure"),
    inputs=[Input("range-min-max", "children")],
    state=[
        State("df-ohlc-stash", "children"),
        State("target-selector", "value"),
        State("base-selector", "value"),
    ],
)
def generate_trend_plot(
    slider_range, jsonified_df, target, base,
):
    """
    Triggers either by range selector or social. When new symbol requested,
    slider_send_update handles request then triggers this callback
    """

    df = pd.read_json(jsonified_df, orient="split")

    if slider_range is not None:
        smin, smax = slider_range.split("|")
        smin = int(smin)
        smax = int(smax)
        df = df.loc[smin:smax, :]

    figure_trend = generate_macd_plot(df, base, target)

    return figure_trend


if __name__ == "__main__":
    app.run_server(debug=False, dev_tools_hot_reload=False)

