import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

DATA_PATH = "BattedBallData.xlsx"
df = pd.read_excel(DATA_PATH)

important_columns = ['LAUNCH_ANGLE', 'EXIT_SPEED', 'EXIT_DIRECTION', 'HIT_DISTANCE', 'HIT_SPIN_RATE']

app = dash.Dash(__name__)
server = app.server

# Define the app layout
app.layout = html.Div([
    html.H1("Batted Ball Data Visualizer", style={"textAlign": "center"}),

    # X-axis dropdown
    html.Div([
        html.Label("Select X-axis:"),
        dcc.Dropdown(
            id="x-axis",
            options=[{"label": col.replace('_', ' ').title(), "value": col} for col in important_columns],
            value="LAUNCH_ANGLE"  
        )
    ], style={"width": "45%", "display": "inline-block"}),

    # Y-axis dropdown
    html.Div([
        html.Label("Select Y-axis:"),
        dcc.Dropdown(
            id="y-axis",
            options=[{"label": col.replace('_', ' ').title(), "value": col} for col in important_columns],
            value="EXIT_SPEED"  # Default Y-axis
        )
    ], style={"width": "45%", "display": "inline-block"}),

    # Graph
    dcc.Graph(id="scatter-plot"),

    # Data summary table
    html.Div(id="data-summary", style={"marginTop": "20px"})
])


@app.callback(
    [Output("scatter-plot", "figure"),
     Output("data-summary", "children")],
    [Input("x-axis", "value"),
     Input("y-axis", "value")]
)
def update_graph(x_col, y_col):
    # Create a scatter plot
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color="PLAY_OUTCOME",  # Change to a column you want for categorical differentiation
        title=f"{y_col.replace('_', ' ').title()} vs {x_col.replace('_', ' ').title()}",
        labels={x_col: x_col.replace('_', ' ').title(), y_col: y_col.replace('_', ' ').title()},
        hover_data=important_columns
    )

    summary = df[[x_col, y_col]].describe().to_dict()
    summary_table = html.Table([
        html.Thead(html.Tr([html.Th("Statistic"), html.Th(x_col), html.Th(y_col)])),
        html.Tbody([
            html.Tr([html.Td(stat), html.Td(round(summary[x_col][stat], 2)), html.Td(round(summary[y_col][stat], 2))])
            for stat in summary[x_col]
        ])
    ])

    return fig, summary_table


if __name__ == "__main__":
    app.run_server(debug=True)
    

