''' A simple coronavirus data visualization program using Plotly '''
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

# Create month and day columns
df['month'] = df['date'].apply(lambda x: int(x.split('-')[1]))
df['day'] = df['date'].apply(lambda x: int(x.split('-')[2]))

# Only grab December for now
MONTH = 12
df = df[(df['location'] != 'World') & (df['month'] == MONTH)]

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='day-slider',
        min=df['day'].min(),
        max=df['day'].max(),
        value=df['day'].min(),
        marks={str(day): str(day) for day in df['day'].unique()},
        step=None
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('day-slider', 'value'))
def update_figure(selected_day):
    filtered_df = df[df['day'] == selected_day]
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

    coronamap = go.Figure(data = [data], layout = layout)

    coronamap.update_layout(transition_duration=500)

    return coronamap

app.run_server(debug=True, use_reloader=True) # Turn off reloader if inside Jupyter
