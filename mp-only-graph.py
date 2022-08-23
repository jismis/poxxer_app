import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

from flask import Flask, jsonify

app = Dash(__name__)
server = app.server
 
# Dash.register_page(__name__,path='/')

# -- Import and clean data (importing csv into pandas)

df = pd.read_csv("https://docs.google.com/spreadsheets/d/12OND1wYiqBGbp2XFmxGgMOItoTG55ojK-FMLmTSh-jU/export?format=csv", index_col=False)
print(df.columns)
name_column = df.columns[-1]


app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_option",
                 options=[
                     {"label": "Today's Cases", "value": name_column}],
                 multi=False,
                 value=name_column,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container'),

    html.Br(),

    dcc.Graph(id='monkeypox_cases')

])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='monkeypox_cases', component_property='figure')],
    [Input(component_id='slct_option', component_property='value')]
)
def update_graph(option_slctd):
    dff = df.copy()
    dff = dff[dff.Province_State != "Total"]
    #dff = dff.drop("Total",axis=1)
    #dff = dff[dff[name_column] == option_slctd]
    container = "showing {}".format(option_slctd)
    # dff = dff[dff["Affected by"] == "Varroa_mites"]
# Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='State_Code',
        scope="usa",
        color=name_column,
        hover_data=['Province_State', name_column],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Province_State': 'State',name_column: 'cases'},
        template='plotly_dark'
    )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)
