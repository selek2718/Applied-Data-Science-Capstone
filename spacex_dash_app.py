# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
#import seaborn as sns
import dash_core_components as dcc
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
                                html.Div([
                                    html.Label('Select Launch Site'),
                                    dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'All Sites'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                             ],
                                             value='All Sites',
                                             placeholder='Select Launch Site',
                                             searchable=True)]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([
                                html.Div(id='success-pie-chart', className='chart-grid', style={'display':'flex'})]),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([
                                html.Div(id='success-payload-scatter-chart', className='chart-grid', style={'display':'flex'})]),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='children'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):   
    if entered_site == 'All Sites':
        filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(filtered_df, values='class', 
                    names= 'Launch Site', 
                    title='Pie Chart of Success Rates for all Launch Sites')
        gra1 = dcc.Graph(figure=fig)
        return [html.Div(className='chart-item', children=[html.Div(children=gra1)],style={'display':'flex'})]
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts().reset_index()
        fig = px.pie(filtered_df, values='count',
                    names='class',
                    title='Pie Chart of Success Rates for site %s'% entered_site)
        gra2 = dcc.Graph(figure=fig)
        return [html.Div(className='chart-item', children=[html.Div(children=gra2)],style={'display':'flex'})]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='children'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_mass):
    if entered_site=='All Sites':
        fil = spacex_df[payload_mass[0]<spacex_df['Payload Mass (kg)']]
        filtered_df = fil[fil['Payload Mass (kg)']<payload_mass[1]]
        fig = px.scatter(filtered_df,
                          x='Payload Mass (kg)',
                          y='class',
                          title='Success by Payload Mass for All Sites')
        gra3 = dcc.Graph(figure=fig)
        return [html.Div(className='chart-item', children=[html.Div(children=gra3)],style={'display':'flex'})]
    else:
        fil = spacex_df[spacex_df['Launch Site']==entered_site]
        filt = fil[payload_mass[0]<fil['Payload Mass (kg)']]
        filtered_df = filt[filt['Payload Mass (kg)']<payload_mass[1]]
        fig = px.scatter(filtered_df,
                          x='Payload Mass (kg)',
                          y='class',
                          title='Success by Payload Mass for %s' % entered_site)
        gra4 = dcc.Graph(figure=fig)
        return [html.Div(className='chart-item', children=[html.Div(children=gra4)],style={'display':'flex'})]
        

# Run the app
if __name__ == '__main__':
    app.run_server()
