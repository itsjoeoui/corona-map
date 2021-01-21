''' A simple coronavirus data visualization program using Plotly '''
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

app.layout = html.Div([
    dcc.Graph(id='graph-with-picker'),
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(2020, 1, 21),
        max_date_allowed=date(2021, 1, 1),
        initial_visible_month=date(2020, 1, 22),
        date=date(2020, 1, 22)
    )
])

@app.callback(
    Output('graph-with-picker', 'figure'),
    Input('my-date-picker-single', 'date'))
def update_figure(date_value):
    filtered_df = df[df['date'] == date.fromisoformat(date_value)]

    data = dict(
        type = 'choropleth',
        locations = filtered_df['iso_code'],
        locationmode = 'ISO-3',
        colorscale = 'burgyl',
        z = filtered_df['total_cases'],
        marker = dict(
            line = dict(color = 'rgb(12,12,12)', width = 1)
        ),
        colorbar = dict(
            title = 'Death Count (M)'
        ),
    )

    layout = dict(
        title = 'COVID-19 Data Visualization',
        geo = dict(
            showframe = True,
            projection = {
                'type':'equirectangular'
            }
        )
    )

    fig = go.Figure(data = [data], layout = layout)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
