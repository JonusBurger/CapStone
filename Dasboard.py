# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(spacex_df["class"])
print(type(spacex_df.loc[1, "class"]))
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                    # Create dropdown
                                dcc.Dropdown(id="site-dropdown",
                                options=[
                                        {'label': 'All sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',
                                    placeholder="Selecet a Launch Site here",
                                    searchable=True,
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max =10000, step=1000,
                                                marks={0: '0',
                                                1000:'1000',
                                                2000:'2000',
                                                3000:'3000',
                                                4000:'4000',
                                                5000:'5000',
                                                6000:'6000',
                                                7000:'7000',
                                                8000:'8000',
                                                9000:'9000',},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site):
    filtered_df = spacex_df
    if site == "ALL":
        fig = px.pie(filtered_df, values='class',
        names = "Launch Site",
        title= 'Success to Failure Ratio ALL sites')
    else:
        df_pie = filtered_df.loc[filtered_df["Launch Site"] == site]
        df_pie["successes"] = ["success" if x==1 else "failed" for x in df_pie["class"] ]
        df_pie["sum"] = [1 for x in df_pie["class"]]
        fig = px.pie(df_pie, values="sum",
        names = "successes",
        title= f'Success to Failure Ratio of {site} Launch Site')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'),
              )
def get_scatter_plot(site, load_val):
    # print('Params: {} {}'.format(site, load_val))	
    filtered_df2 = spacex_df.loc[spacex_df["Payload Mass (kg)"] <=load_val[1]]
    filtered_df2 = filtered_df2.loc[filtered_df2["Payload Mass (kg)"] >=load_val[0]]
    # filtered_df2 = spacex_df
    if site == "ALL":
        fig = px.scatter(filtered_df2, x="Payload Mass (kg)", y="class", color="Booster Version Category",
        title="Successes for all Launch Sites and Payload Range between {} and {} Kg".format(load_val[0], load_val[1]))
    else:
        df_scatter = filtered_df2.loc[filtered_df2["Launch Site"] == site]
        fig = px.scatter(df_scatter, x="Payload Mass (kg)", y="class", color="Booster Version Category",
        title="Successes for Launch Site {} and Payload Range between {} and {} Kg".format(site, load_val[0], load_val[1]))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
