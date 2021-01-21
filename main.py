''' A simple coronavirus data visualization program using Plotly '''
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')

data = dict(
    type = 'choropleth',
    locations = df['iso_code'],
    locationmode = 'ISO-3',
    colorscale = 'burgyl',
    z = df[df['location'] != 'World']['total_cases'],
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

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(figure=coronamap)
])

app.run_server(debug=True, use_reloader=True) # Turn off reloader if inside Jupyter

# iplot(coronamap)
