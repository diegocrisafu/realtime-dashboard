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

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


# Create a deque to store a fixed number of data points
MAX_LENGTH = 50
y_data = collections.deque(maxlen=MAX_LENGTH)
x_data = collections.deque(maxlen=MAX_LENGTH)


def update_data(n):
    """Generate the next data point and append it to the series."""
    if len(x_data) == 0:
        x = 0
        y = random.uniform(0, 10)
    else:
        x = x_data[-1] + 1
        y = y_data[-1] + random.uniform(-1, 1)
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
    dcc.Graph(id='live‑graph', animate=True),
    dcc.Interval(
        id='interval‑component',
        interval=1_000,  # update every 1000 ms
        n_intervals=0
    ),
    html.Div([
        html.P('This graph updates once per second with simulated data. Replace the data generation logic in update_data() with your own data source to visualise real metrics.', style={'textAlign': 'center'})
    ], style={'maxWidth': '600px', 'margin': '0 auto'})
])


@app.callback(
    Output('live‑graph', 'figure'),
    Input('interval‑component', 'n_intervals')
)
def update_graph_live(n):
    """Callback to update the graph at each interval."""
    update_data(n)
    return create_figure()


if __name__ == '__main__':
    # When running locally, enable hot reloading and debugging.
    app.run_server(debug=True)