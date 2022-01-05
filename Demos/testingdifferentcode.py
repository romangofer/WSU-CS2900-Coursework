import plotly.graph_objects as go
import numpy as np
np.random.seed(42)

# Simulate data
returns = np.random.normal(0.01, 0.2, 100)
price = 100 * np.exp(returns.cumsum())
time = np.arange(100)

# Generate graph using Figure Constructor
layout = go.Layout(
    title="Historic Prices",
    xaxis_title="time",
    yaxis_title="price"
)

fig = go.Figure(
    data=go.Scatter(x=time, y=price),
    layout=layout
)
fig.show()