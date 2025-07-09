import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("spacex_full_data.csv")

# Filter out rows with missing values in required columns
df = df.dropna(subset=['launch_site', 'payload_mass_kg', 'landing_success'])

# Get unique launch sites
launch_sites = df['launch_site'].unique()
options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Dashboard', style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='site-dropdown',
        options=options,
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload Mass Range (kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=df['payload_mass_kg'].min(),
        max=df['payload_mass_kg'].max(),
        step=100,
        value=[df['payload_mass_kg'].min(), df['payload_mass_kg'].max()],
        marks={int(df['payload_mass_kg'].min()): 'Min', int(df['payload_mass_kg'].max()): 'Max'}
    ),

    dcc.Graph(id='success-payload-scatter')
])

# Callback: Pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(df, names='launch_site', title='Total Launches by Site')
    else:
        filtered = df[df['launch_site'] == selected_site]
        fig = px.pie(filtered, names='landing_success',
                     title=f'Success vs Failure at {selected_site}',
                     labels={0: 'Failure', 1: 'Success'})
    return fig

# Callback: Scatter plot
@app.callback(
    Output('success-payload-scatter', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    filtered_df = df[
        (df['payload_mass_kg'] >= payload_range[0]) &
        (df['payload_mass_kg'] <= payload_range[1])
    ]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['launch_site'] == selected_site]

    fig = px.scatter(
        filtered_df,
        x='payload_mass_kg',
        y='landing_success',
        color='rocket_name',
        title='Payload vs Landing Success'
    )
    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
