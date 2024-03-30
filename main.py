from dash import Dash, html, dcc, Input, Output
from builders import make_table
from data import countries_df, totals_df, dropdown_options, make_global_df, make_country_df
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
    size_max=40,
    hover_name="Country_Region",
    color="Confirmed", 
    color_continuous_scale=px.colors.sequential.OrRd,  
    locationmode="country names",
    locations="Country_Region", 
    title="Confirmed by Country",
    template="plotly_dark",
    projection="natural earth",
    hover_data={
        "Confirmed": ":,.2f",
        "Recovered": ":,.2f",
        "Deaths": ":,.2f",
        "Country_Region": False
    }
)

bubble_map.update_layout(
    margin=dict(l=0,r=0,t=40, b=0)
)

bars_graph = px.bar(
    totals_df, 
    x="condition", 
    y="count", 
    hover_data={'count': ":,"},
    template="plotly_dark", 
    title="Total Global Cases",
    labels={"condition": "Condition", "count": "Count", "color": "Condition"}
)

bars_graph.update_layout (
    xaxis=dict(title="Condition"),
    yaxis=dict(title="Count")
)

bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "minHeight": "100vh", 
        "backgroundColor": "black", 
        "color": "white", 
        "fontFamily": "Open Sans, sans-serif"
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": "100px"}, 
            children=[html.H1("Corona Dashboard", style={"fontSize": "40px"})]
        ),
        html.Div(
            style={"display": "grid", 
                   "gap": "50px", 
                   "gridTemplateColumns": "repeat(4, 1fr)"
                   },
            children=[
                html.Div(
                    style={"gridColumn": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)]  # Placeholder for the graph, you need to provide the actual graph component
                ),
                html.Div(children=[make_table(countries_df)])
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": "50px",
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(id="country_graph", figure=bars_graph)]),  # Corrected ID
                html.Div(children=[
                    html.Div(
                        style={"gridColumn": "span 3"},
                        children=[
                        dcc.Dropdown(
                            style={
                                "width":320,
                                "margin":"0 auto",
                                "color": "#11111",
                            },
                            placeholder="Select a Country",
                            id="country",
                                     options=[{'label': country, 'value': country} 
                                              for country in dropdown_options]
                        )
                    ]),
                    dcc.Graph(id="country_graph")  
                ]),
            ],
        ),
    ],
)

@app.callback(Output("country_graph", "figure"), [Input("country", "value")])
def update_country_graph(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()

   
    fig = px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={"value": "Cases", "variable": "Condition", "date": "Date"},
        hover_data={"value": ":,", "variable": False, "date": False},
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
