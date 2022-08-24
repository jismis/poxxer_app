##adding increased cases to each of the states
import numpy as np
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

from flask import Flask, jsonify

app = Dash(__name__)
server = app.server

df = pd.read_csv("https://docs.google.com/spreadsheets/d/12OND1wYiqBGbp2XFmxGgMOItoTG55ojK-FMLmTSh-jU/export?format=csv", index_col=False)
current_reported_date = df.columns[-1]
previous_reported_date = df.columns[-2]

print(df.columns[-1])


##create column for difference between two columns

def diff(a, b):
    return b - a

df['Difference_in_Cases'] = df.apply(
    lambda x: diff(x[previous_reported_date], x[current_reported_date]), axis=1)

# print(df.columns)
print(df[:5])

app.layout = html.Div([

    html.H1("Monkeypox Cases in USA", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_option",
                 options=[
                     {"label": "Today's Cases", "value": current_reported_date}
                    #  {"label": "Case Increase ", "value": current_reported_date}
                     ],
                 multi=False,
                 value=current_reported_date,
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
    dff = dff[dff.Province_State != "Total"] ##takes total out of rows i think
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
        color=current_reported_date,
        hover_data=['Province_State', current_reported_date,'Difference_in_Cases'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Province_State': 'State', current_reported_date: 'Total Cases', 'Difference_in_Cases': 'Case Increase'},
        template='plotly_dark'
    )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)