"""
Real‑Time Data Visualisation Dashboard
=====================================

This simple dashboard uses the Dash framework to display a live‑updating line
chart.  At each interval the application appends a random value to the data
series, simulating a data stream.  The graph refreshes automatically in
the browser without requiring a page reload.

To run the app locally:

    pip install -r requirements.txt
    python app.py

Then navigate to http://127.0.0.1:8050 in your browser.  The chart will
update every second.
"""

import random
import collections
import math

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


# Create a deque to store a fixed number of data points
MAX_LENGTH = 50
y_data = collections.deque(maxlen=MAX_LENGTH)
x_data = collections.deque(maxlen=MAX_LENGTH)


def update_data(n, source='random'):
    """Generate the next data point and append it to the series based on the selected data source."""
    # Determine next x value
    x = 0 if len(x_data) == 0 else x_data[-1] + 1
    # Generate y based on data source
    if source == 'sine':
        # Use a sine wave with gradually increasing x
        y = 5 * math.sin(x / 5.0) + 5  # shift up to keep values positive
    else:
        # Default to random walk
        if len(y_data) == 0:
            y = random.uniform(0, 10)
        else:
            y = y_data[-1] + random.uniform(-1, 1)
    # Append values to deques
    x_data.append(x)
    y_data.append(y)


def create_figure():
    """Construct a Plotly figure from the current data series."""
    return {
        'data': [go.Scatter(
            x=list(x_data),
            y=list(y_data),
            mode='lines+markers',
            line={'color': '#4b86b4'},
            marker={'size': 6}
        )],
        'layout': go.Layout(
            xaxis={'title': 'Time', 'range': [max(0, x_data[0] if x_data else 0), x_data[-1] if x_data else 0]},
            yaxis={'title': 'Value'},
            margin={'l': 40, 'r': 10, 't': 40, 'b': 40},
            hovermode='closest',
            title='Real‑Time Data Stream'
        )
    }


app = dash.Dash(__name__)
server = app.server  # for deployment on platforms like Heroku

app.layout = html.Div([
    html.H1('Real‑Time Data Visualisation Dashboard', style={'textAlign': 'center', 'color': '#2a4d69'}),
    # Controls: data source selection and update interval
    html.Div([
        html.Label('Data Source:', style={'marginRight': '8px'}),
        dcc.Dropdown(
            id='data-source',
            options=[
                {'label': 'Random Walk', 'value': 'random'},
                {'label': 'Sine Wave', 'value': 'sine'},
            ],
            value='random',
            clearable=False,
            style={'width': '200px', 'display': 'inline-block', 'marginRight': '20px'}
        ),
        html.Label('Update Interval (ms):', style={'marginRight': '8px'}),
        dcc.Slider(
            id='update-interval',
            min=500,
            max=5000,
            step=500,
            value=1000,
            marks={
                500: {'label': '0.5s'},
                1000: {'label': '1s'},
                2000: {'label': '2s'},
                3000: {'label': '3s'},
                4000: {'label': '4s'},
                5000: {'label': '5s'},
            },
            tooltip={'placement': 'bottom', 'always_visible': False},
            style={'width': '300px', 'display': 'inline-block'}
        ),
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'marginBottom': '20px', 'gap': '20px'}),
    dcc.Graph(id='live‑graph', animate=True),
    # Interval component will be controlled by slider
    dcc.Interval(
        id='interval‑component',
        interval=1000,
        n_intervals=0
    ),
    html.Div([
        html.P('This graph updates based on your selected interval with simulated data. Replace the data generation logic in update_data() with your own data source to visualise real metrics.', style={'textAlign': 'center'})
    ], style={'maxWidth': '600px', 'margin': '0 auto'})
])


@app.callback(
    Output('interval‑component', 'interval'),
    Input('update-interval', 'value')
)
def update_interval(interval_value):
    """Update the interval of the Interval component based on slider."""
    return interval_value


@app.callback(
    Output('live‑graph', 'figure'),
    Input('interval‑component', 'n_intervals'),
    Input('data-source', 'value')
)
def update_graph_live(n, source):
    """Callback to update the graph at each interval."""
    update_data(n, source)
    return create_figure()


if __name__ == '__main__':
    # When running locally, enable hot reloading and debugging.
    app.run_server(debug=True)