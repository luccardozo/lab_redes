import pandas as pd
import plotly
from plotly import graph_objs as go
import sys


LABEL_X = 'Time'
LABEL_Y = '[Mb/s]'

if len(sys.argv) is not 2:
    print("Wrong format. Enter: python plot <number_of_connections>")
    exit()

numberOfConnections = int(sys.argv[1])
data = []
fig = None

for x in range(numberOfConnections):
    df = pd.read_csv('results%s.csv' % x)
    trace = go.Scatter(
        x = df[LABEL_X].tolist(),
        y = df[LABEL_Y].tolist(),
        mode = 'lines',
        name = 'Connection %d' % x
    )
    data.append(trace)

fig = go.Figure(data=data)
fig.show()