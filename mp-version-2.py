##adding increased cases to each of the states

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

from flask import Flask, jsonify

app = Dash(__name__)
server = app.server

df = pd.read_csv("https://docs.google.com/spreadsheets/d/12OND1wYiqBGbp2XFmxGgMOItoTG55ojK-FMLmTSh-jU/export?format=csv", index_col=False)
print(df.columns)
todays_date = df.columns[-1]