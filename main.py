''' A simple coronavirus data visualization program using Plotly '''
import requests
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot

URL = "https://coronavirus-tracker-api.herokuapp.com/v2/locations"

response = requests.get(URL)

df = pd.DataFrame(response.json()['locations'])

df['confirmed'] = df['latest'].apply(lambda count: count['confirmed'])

data = dict(
    type = 'choropleth',
    locations = df['country'],
    locationmode = 'country names',
    colorscale = 'burgyl',
    z = df['confirmed'],
    marker = dict(
        line = dict(color = 'rgb(12,12,12)', width = 1)
    ),
    colorbar = {'title':'Death Count (M)'},
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

iplot(coronamap)
