import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# -------------------------
# Initialize Flask App
# -------------------------
server = Flask(__name__)

# --------------------------
# Load and Process Data
# --------------------------
data = pd.read_csv('data/LO-GLBM.csv', skiprows=1)

#Check column names and preview data
print("Columns in the dataset:")
print(data.columns)
print("First 145 rows of data:")
print(data.head())
print(data.tail())

# Add a column for decades (e.g., 1980 for years 1980-1989)
data['Decade'] = (data['Year'] // 10) * 10

# Convert monthly columns to numeric (coerce errors to NaN)
columns_to_convert = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
data[columns_to_convert] = data[columns_to_convert].apply(pd.to_numeric, errors='coerce')

# Calculate the annual average temperature anomaly
data['Annual Average'] = data[columns_to_convert].mean(axis=1)

# Verify the Annual Average calculation
print("First few rows with Annual Average:")
print(data[['Year', 'Annual Average']].head())

# Group the data by decade and compute the mean anomaly
decade_avg = data.groupby('Decade')['Annual Average'].mean().reset_index()

# Print the calculated decade averages
print("Decade averages:")
print(decade_avg)

plt.figure(figsize=(10, 6))
plt.bar(decade_avg['Decade'], decade_avg['Annual Average'], color='orange', width=8)
plt.title('Average Temperature Anomalies by Decade', fontsize=16)
plt.xlabel('Decade', fontsize=14)
plt.ylabel('Temperature Anomaly (°C)', fontsize=14)
plt.grid(axis='y')
# plt.show()  # Comment this out so it doesn't block the Flask server

# --------------------------
# Initialize Dash App with Flask Server
# --------------------------
app = Dash(__name__, server=server, url_base_pathname="/dashboard/")

# Plotly bar chart
fig = px.bar(
    decade_avg,
    x='Decade',
    y='Annual Average',
    title='Average Temperature Anomalies by Decade',
    labels={'Decade': 'Decade', 'Annual Average': 'Temperature Anomaly (°C)'},
    color_discrete_sequence=['orange']
)
fig.update_layout(
    xaxis=dict(title='Decade'),
    yaxis=dict(title='Temperature Anomaly (°C)'),
    title=dict(font=dict(size=24))
)

# Line chart for annual anomalies over time
line_fig = px.line(
    data,
    x='Year',
    y='Annual Average',
    title='Annual Temperature Anomalies Over Time',
    labels={'Year': 'Year', 'Annual Average': 'Temperature Anomaly (°C)'}
)
line_fig.update_layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Temperature Anomaly (°C)'),
    title=dict(font=dict(size=24))
)

# Assume line_fig has been defined earlier as a Plotly line chart, for example:
line_fig = px.line(
    data,
    x='Year',
    y='Annual Average',
    title='Annual Temperature Anomalies Over Time',
    labels={'Year': 'Year', 'Annual Average': 'Temperature Anomaly (°C)'}
)
line_fig.update_layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Temperature Anomaly (°C)'),
    title=dict(font=dict(size=24))
)

# Define the layout with a dropdown and two graph components
app.layout = html.Div([
    html.H1('Temperature Anomalies Dashboard', style={'textAlign': 'center'}),
    
    # Dropdown for interactive selection
    dcc.Dropdown(
        id='anomaly-type',
        options=[
            {'label': 'Annual Average', 'value': 'Annual Average'},
            {'label': 'Winter (DJF)', 'value': 'DJF'},
            {'label': 'Spring (MAM)', 'value': 'MAM'},
            {'label': 'Summer (JJA)', 'value': 'JJA'},
            {'label': 'Fall (SON)', 'value': 'SON'}
        ],
        value='Annual Average',  # default value
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    # First graph: This one will update via a callback based on the dropdown
    dcc.Graph(id='anomaly-graph'),
    
    # Second graph: A static line chart (or you can update it with a callback as well)
    dcc.Graph(id='line-chart', figure=line_fig)
])


# Callback to update the graph based on dropdown selection
@app.callback(
    Output('anomaly-graph', 'figure'),
    [Input('anomaly-type', 'value')]
)
def update_graph(selected_anomaly):
    # 'decade_avg' DataFrame
    fig = px.bar(
        decade_avg,
        x='Decade',
        y=selected_anomaly,
        title=f'{selected_anomaly} Temperature Anomalies by Decade',
        labels={'Decade': 'Decade', selected_anomaly: 'Temperature Anomaly (°C)'},
        color_discrete_sequence=['orange']
    )
    fig.update_layout(
        xaxis=dict(title='Decade'),
        yaxis=dict(title='Temperature Anomaly (°C)'),
        title=dict(font=dict(size=24))
    )
    return fig


# --------------------------
# Define Flask Route for Homepage
# --------------------------
@server.route("/")
def index():
    return "<h1>Welcome to the Climate Dashboard</h1><p>Visit <a href='/dashboard/'>Dashboard</a></p>"

# --------------------------
# Run the Integrated App
# --------------------------
if __name__ == "__main__":
    # Running the Flask server will serve both the Flask routes and the Dash app
    server.run(debug=True, port=5000)
