from dash import Dash, html, dcc


def make_table(df):
    return html.Table(
        children=[
            html.Thead(style={"display": "block", "marginBottom": 30},
                children=[
                    html.Tr(
                        children=[
                            html.Th(column_name.replace("_", " ")) for column_name in df.columns
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "fontWeight": "600",
                            "fontSize": 15,
                        },
                    )
                ],
            ),
            html.Tbody(
                style={"maxHeight": "50vh", "display": "block", "overflow": "scroll",},                                 
                children=[
                    html.Tr(style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "border-top": "1px solid white",
                            "padding": "30px 0px",
                            "backgroundColor": "black"
                        },
                        children=[html.Td(value_column) for value_column in value]
                    ) for value in df.values
                ]
            )
        ]
    )
