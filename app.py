# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import flask
import dash

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State, Event


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash()
# = app.server
# 数据载入


df = pd.read_csv('data/jjwcut.csv')
# app的layout 
ava_PointName=df['PointName'].unique()

app.layout = html.Div([
        html.H1(
                '成都栖睿',
                 style={
            'textAlign': 'center',
            'color': '#7FDBFF'
         }
        ),
        html.Div(children='''
        纪检委数据
    ''',
    style={
            'textAlign': 'center',
            'color': '#7FDBFF'}
    ),
           
    html.Div([
        html.Label('请选择PointName'),
        html.Div([
            dcc.Dropdown(   # 功能性组件， 设定id值作为标签关联callback函数中的标签
                id='PointName',
                options=[{'label': i, 'value': i} for i in ava_PointName],
                value='PointName'),
        ]),
        
    ], className="three columns"),  # 直接加入css的功能
    html.Div([
        dcc.Graph(id='scatter1')    # 关联graph
    ], className="eight columns")
], className="page")

# 对callback函数进行设置， 与上面的对应， 将数据return回对应id的Graph
@app.callback(
    dash.dependencies.Output('scatter1', 'figure'),
    [dash.dependencies.Input('PointName','value')
     ]
)
def update_scatter(value_Value):
    grouped = df.groupby('PointName')  
    data = grouped.get_group(value_Value) 
   
    trace = go.Scatter(
                x=data['Date'],
                y=data["Value"],
              #mode='lines',
                marker=dict(
                   # size=s,
                    sizemode='diameter',
                    sizeref=0,
                    #color=color_class.codes,
                    colorscale='Earth'
                ))

    layout = go.Layout(margin=dict(l=20, r=20, t=0, b=30)) #切边
    fig = go.Figure(data=[trace], layout=layout)
    return fig



if __name__ == '__main__':
    app.run_server( debug=True)

