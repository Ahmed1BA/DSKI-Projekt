import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Bundesliga Dashboard", style={'textAlign': 'center', 'fontFamily': 'Arial'}),
            style={"border": "0px solid black", "padding": "10px", "height": "20vh", "backgroundColor": "#838b8b"}
        )
    ]),
    dbc.Row([
       dbc.Col([
            html.H5("Auswahl des Spiels", style={"fontSize": "24px", "fontWeight": "bold", "color": "#343a40"}),
            dcc.RadioItems(
                id='spiel-auswahl',
                options=[
                    {'label': f'Spiel {i}', 'value': f'spiel_{i}'} for i in range(1, 11)
                ],
                value='spiel_1',  # Standardmäßig ausgewähltes Spiel
                labelStyle={"display": "block", "cursor": "pointer", "margin": "5px 0"}
            )
        ], width=2, style={"border": "1px solid black", "padding": "10px", "height": "100vh", "backgroundColor": "#f8f9fa"}),


        # Mannschaft A
        dbc.Col([
            html.H5("Mannschaft A"),
            html.Ul([html.Li(player) for player in ['A', 'B', 'V', 'D', 'F', 'D', 'G', 'S']])
        ], width=3, style={"border": "0px solid black", "padding": "10px", "height": "100vh"}),

        # Mannschaft B
        dbc.Col([
            html.H5("Mannschaft B"),
            html.Ul([html.Li(player) for player in ['A', 'B', 'V', 'D', 'F', 'D', 'G', 'S', 'T']])
        ], width=3, style={"border": "0px solid black", "padding": "10px", "height": "100vh"}),

        # Textausgabe Gemini
        dbc.Col([
            html.H5("TextOutput Gemini"),
            html.Div(id="text-output", children="Hier erscheint der Textoutput")
        ], width=2, style={"border": "0px solid black", "padding": "10px", "height": "100vh"}),
    ]),
    dbc.Row([
        dbc.Col(
            style={"border": "0px solid black", "padding": "10px", "height": "20vh", "backgroundColor": "#838b8b"}
        )
    ]),
], fluid=True)



@app.callback(
    [Output("mannschaft-a", "children"), Output("mannschaft-b", "children")],
    [Input("spiel-auswahl", "value")]
)
def update_teams_callback(selected_game):
    return update_teams(selected_game)
def update_text_output(selected_games):
    if selected_games:
        return f"Ausgewählte Spiele: {', '.join(selected_games)}"
    return "Bitte mindestens ein Spiel auswählen"


if __name__ == '__main__':
    app.run_server(debug=True)
