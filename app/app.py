import pandas as pd
import os
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Load data
df = pd.read_csv('data/owid-energy-data.csv')

# Filter out rows with no country name or no year
df = df[df['country'].notna() & df['year'].notna()]

# List of energy types we want to show
energy_options = {
    'coal_consumption': 'Coal',
    'oil_consumption': 'Oil',
    'gas_consumption': 'Natural Gas',
    'renewables_consumption': 'Renewables',
    'nuclear_consumption': 'Nuclear'
}

# Initialize Dash app
app = Dash(__name__)
app.title = "World Energy Dashboard"

# Layout
app.layout = html.Div([
    html.H1("🌍 World Energy Consumption Dashboard"),

    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in sorted(df['country'].unique())],
            value=['India', 'United States'],
            multi=True
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        html.Label("Select Energy Type:"),
        dcc.Dropdown(
            id='energy-dropdown',
            options=[{'label': name, 'value': key} for key, name in energy_options.items()],
            value='oil_consumption',
            multi=False,
            clearable=False 
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='energy-graph')
    ], className="graph-container"),

    html.Div([
    dcc.Graph(id='energy-map')
      ], className="map-container"),

    html.Div([
        html.Button("Download CSV", id="btn_download", className="btn btn-primary"),
        dcc.Download(id="download_data")
    ], style={"marginTop": "20px", "textAlign": "center"})
])


# Callback to update graph
@app.callback(
    Output('energy-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('energy-dropdown', 'value')

)
def update_graph(selected_countries, selected_energy):
    if not isinstance(selected_countries, list):
        selected_countries = [selected_countries]

    filtered_df = df[
        (df['country'].isin(selected_countries)) & 
        (df['year'] >= 1960)
    ]
    fig = px.line(
        filtered_df,
        x='year',
        y=selected_energy,
        color='country',
        title="Consumption Over Time",
        labels={'year': 'Year', selected_energy: 'Energy (TWh)'}
    )
    fig.update_layout(transition_duration=500)
   


    return fig

@app.callback(
    Output('energy-map', 'figure'),
    Input('energy-dropdown', 'value')
)
def update_map(selected_energy):
    # Filter from 2000 to 2024
    filtered_df = df[(df['year'] >= 2000) & (df['year'] <= 2024)]

    # Group by country and sum the energy consumption
    agg_data = (
        filtered_df.groupby(['country', 'iso_code'], as_index=False)[selected_energy]
        .sum()
        .rename(columns={selected_energy: 'total_consumption'})
    )

    # Fill NaNs with 0
    agg_data['total_consumption'] = agg_data['total_consumption'].fillna(0)

    fig = px.choropleth(
        agg_data,
        locations='iso_code',
        color='total_consumption',
        hover_name='country',
        color_continuous_scale='Viridis',
        title=f"Total {energy_options[selected_energy]} Consumption (2000–2024)"
    )

    fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    plot_bgcolor='white',  # map chart background stays white
    paper_bgcolor=' dark grey',
    font_color='black'  # use black text to contrast on white
        
    )
    return fig


@app.callback(
    Output("download_data", "data"),
    Input("btn_download", "n_clicks"),
    State("country-dropdown", "value"),
    State("energy-dropdown", "value"),
    prevent_initial_call=True
)
def download_csv(n_clicks, selected_countries, selected_energy):
   filtered_df = df[
        (df["country"].isin(selected_countries)) & 
        (df["year"] >= 1960)
    ][["country", "year", selected_energy]]

   return dcc.send_data_frame(
        filtered_df.to_csv,
        f"{selected_countries}_{selected_energy}.csv",
        index=False
    )

# Run server


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8051)))