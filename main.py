'''A simple coronavirus data visualization program using Plotly'''
from datetime import date
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

df['date'] = df['date'].apply(date.fromisoformat)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

links = {
    "home": "https://itsjoeoui.com/",
    "github": "https://github.com/itsjoeoui/corona-map"
}

jumbotron = dbc.Jumbotron(
    [
        html.H1("COVID-19 Data Visualization", className="display-3"),
        html.P(
            "A simple coronavirus data visualization program using Plotly",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P("Made with love by Joey Yu"),
        html.P([
            dbc.Button("Learn more", color="primary", className="mr-1", href=links['github']),
            dbc.Button("Return to home", color="secondary", className="mr-1", href=links['home'])
        ])
    ]
)

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Projection"),
                dcc.Dropdown(
                    id="projection-type-dropdown",
                    options=[
                        {'label': 'Equirectangular', 'value': 'equirectangular'},
                        {'label': 'Orthographic', 'value': 'orthographic'},
                        {'label': 'Natural earth', 'value': 'natural earth'}
                    ],
                    value='equirectangular'
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[
                        {"label": i, "value": i} for i in {i.year for i in df['date']}
                    ],
                    value=df.iloc[-1]['date'].year
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Month"),
                dcc.Dropdown(
                    id="month-dropdown",
                    options=[
                        {"label": i, "value": i} for i in {i.month for i in df['date']}
                    ],
                    value=df.iloc[-1]['date'].month
                )
            ]
        )
    ],
    body=True
)

slider = dcc.Slider(
    id='day-slider',
    min=1,
    max=31,
    marks={str(day): str(day) for day in range(32)},
    value=df.iloc[-1]['date'].day
)

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(jumbotron, md=12)
        ),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id='graph-with-picker'), md=8),
            ],
            align="center"
        ),
        dbc.Row(
            dbc.Col(slider, md=12)
        )
    ],
    fluid=False
)

@app.callback(
    Output('graph-with-picker', 'figure'),
    [
        Input('projection-type-dropdown', 'value'),
        Input('year-dropdown', 'value'),
        Input('month-dropdown', 'value'),
        Input('day-slider', 'value')
    ]
)
def update_figure(projection_type, year, month, day):
    filtered_df = df[df['date'] == date(year, month, day)]

    data = dict(
        type='choropleth',
        locations=filtered_df['iso_code'],
        locationmode='ISO-3',
        colorscale='burgyl',
        z=filtered_df['total_cases'],
        marker=dict(
            line=dict(color='rgb(12,12,12)', width=1)
        ),
        colorbar=dict(
            title='Death Count (M)'
        ),
        zmin=0,
        zmax=30 * 10 ** 6
    )

    layout = dict(
        geo=dict(
            showframe=True,
            showocean=True, oceancolor="LightBlue",
            showlakes=True, lakecolor="Blue",
            showrivers=True, rivercolor="Blue",
            projection={
                'type':projection_type
            }
        )
    )

    fig = go.Figure(data=[data], layout=layout)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
