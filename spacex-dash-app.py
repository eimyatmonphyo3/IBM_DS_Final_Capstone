# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                             value='All',
                                             placeholder = "Select a Launch Site here",
                                             searchable = True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(input_site):
    if input_site == 'ALL':
        data = spacex_df
        fig = px.pie(data, values='class', names='Launch Site',
                title='Total Success Launch Propotion by Different Sites Pie Chart')
        return fig
    else:
        data = (spacex_df
            .loc[spacex_df['Launch Site'] == input_site]
            .groupby('class')[['class']]
            .count()
            .rename({"class":"count"}, axis=1)
            .reset_index()
        )
        fig = px.pie(data, values='count', names='class',
                title=f'Pie Chart for Total Success Launch of "{input_site}"')
        return fig 

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
              )
def get_success_scatter_plot(input_site, input_payload):
    min_payload = input_payload[0]
    max_payload = input_payload[1]
    data = spacex_df.loc[
        (spacex_df['Payload Mass (kg)'] >= min_payload) &
        (spacex_df['Payload Mass (kg)'] <= max_payload)
    ]
    if input_site == 'ALL':
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                title=f'Scatter Plot showing the relation between Payload and Success for all Sites')
        return fig
    else:
        data = data.loc[data['Launch Site'] == input_site]
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                title=f'Scatter Plot showing the relation between Payload and Success for "{input_site}"')
        return fig

# Run the app
if __name__ == '__main__':
    app.run()
