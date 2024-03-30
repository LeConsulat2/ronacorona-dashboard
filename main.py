from dash import Dash, html, dcc, Input, Output
from builders import make_table
from data import countries_df, totals_df
import plotly.express as px
import pandas as pd

# External stylesheets
stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.2/reset.min.css", 
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"
]

# Initialize Dash app
app = Dash(__name__, external_stylesheets=stylesheets)

# Create bubble map figure
bubble_map = px.scatter_geo(
    countries_df,
    size="Confirmed",
    hover_name="Country_Region",
    color="Confirmed",
    locations="Country_Region",
    locationmode="country names",
    size_max=40,
    title="Confirmed By Country",
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel,
    projection="natural earth",
    hover_data={
        "Confirmed": ":,",
        "Deaths": ":,",
        "Recovered": ":,",
        "Country_Region": False,
    },
)
bubble_map.update_layout(margin=dict(l=0, r=0, t=50, b=0))

# Create bars graph figure
bars_graph = px.bar(
    totals_df,
    x="condition",
    hover_data={"count": ":,"},
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
)
bars_graph.update_layout(xaxis=dict(title="Condition"), yaxis=dict(title="Count"))
bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

# Define app layout
app.layout = html.Div(
    style={
        "minHeight": "100vh", 
        "backgroundColor": "black", 
        "color": "white", 
        "fontFamily": "Open Sans, sans-serif"
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"}, 
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})]
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bubble_map)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[make_table(countries_df)],
                ),
            ]
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    children=[
                        dcc.Input(placeholder="What is your name?", id="hello-input"),
                        html.H2(children="Hello Anonymous", id="hello-output"),
                    ],
                ),
            ]
        ),
    ]
)

@app.callback(
    Output("hello-output", "children"),
    [
        Input("hello-input", "value")
    ]
)

def update_hello(value):
    if value is None:
        return "Hello Anonymous"
    else:
        return f"Hello {value}"


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
