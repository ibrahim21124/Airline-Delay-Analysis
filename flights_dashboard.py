# Importing Dependencies
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Downloading Data
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Creating Dash App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
                        html.H1('Flight Delay Time Statistics',
                                style={'textAlign': 'center', 'color': '#503D36','font-size': 50}),
                                
                                
                        html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', 
                                                            style={'height':'35px', 'font-size': 30}),], 
                                style={'font-size': 30}),
                        
                        html.Br(),
                        html.Br(), 
                        
                        # Segment 1
                        html.Div([
                                html.Div(dcc.Graph(id='carrier-plot')),
                                html.Div(dcc.Graph(id='weather-plot'))
                        ], style={'display': 'flex'}),
                        # Segment 2
                        html.Div([
                                html.Div(dcc.Graph(id='nas-plot')),
                                html.Div(dcc.Graph(id='security-plot'))
                        ], style={'display': 'flex'}),
                        # Segment 3
                        html.Div(dcc.Graph(id='late-plot'), style={'width':'65%'})
            ])

# Helper function to Compute Information
def compute_data(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    print("Compute")
    # Compute Delay Averages
    avg_carrier = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_security = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    
    return avg_carrier, avg_weather, avg_NAS, avg_security, avg_late


# CallBack Function
@app.callback([
               Output(component_id='carrier-plot', component_property='figure'),
               Output(component_id='weather-plot', component_property='figure'),
               Output(component_id='nas-plot', component_property='figure'),
               Output(component_id='security-plot', component_property='figure'),
               Output(component_id='late-plot', component_property='figure')
               ],
               Input(component_id='input-year', component_property='value'))
# Computation to callback function and return graph
def get_graph(entered_year):
    avg_carrier, avg_weather, avg_NAS, avg_security, avg_late = compute_data(airline_data, entered_year)
    
    # Create Plots
    carrier_plot = px.line(avg_carrier, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average Carrier Delay Time by Airline')
    weather_plot = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average Weather Delay Time by Airline')
    NAS_plot = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS Delay Time by Airline')
    security_plot = px.line(avg_security, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average Security Delay Time by Airline')
    late_plot = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average Late Aircraft Delay Time by Airline')
    
    return[carrier_plot, weather_plot, NAS_plot, security_plot, late_plot]

if __name__ == "__main__":
    app.run_server()
