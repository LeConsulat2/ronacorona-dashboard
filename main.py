from dash import Dash, html, dcc
from builders import make_table
from data import countries_df
import plotly.express as px
import pandas as pd

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.2/reset.min.css", 
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"
    
]

app = Dash(__name__, external_stylesheets=stylesheets)

bubble_map = fig = px.scatter_geo(
    countries_df, 
    size="Confirmed",
    size_max=40,
    hover_name="Country_Region",
    color="Confirmed", 
    locationmode="country names",
    locations="Country_Region", 
    template="plotly_dark",
    hover_data={
        "Confirmed": ":,.2f",
        "Recovered": ":,.2f",
        "Deaths": ":,.2f",
        "Country_Region": False
    }
)


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
            children=[html.H1("Corona Dashboard", style={"fontSize":40})]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(figure=bubble_map),  # Placeholder for the graph, you need to provide the actual graph component
                        make_table(countries_df)                       
                    ]
                )
            ]
        )    
    ]
)

map_figure = px.scatter_geo(countries_df)
map_figure.show()



if __name__ == '__main__':
    app.run_server(debug=True)
