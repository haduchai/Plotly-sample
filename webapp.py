import pandas as pd
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, Input, Output, State, callback, ctx
from elements import *

STYLE_={
    'border': '1px solid #000',  # Đặt viền đen độ dày 1px
    'padding': '20px',  # Đặt lề bên trong là 10px
    'border-radius': '10px',  # Đặt viền cong với bán kính 5px,
    'display': 'inline-block',
    'color': 'white',
    'background-color': 'teal',
    'width': '30%',
    'height':'100%',
    'text-align': 'center',
}
STYLE_DROPDOW={
    'width': '200px', 
    'display': 'inline-block', 
}
STYLE_TITLE_GRAPH={
    'text-align': 'center',
    'color':'teal',
    'font-size':'1rem',
    'font-weight': 'bold'
}
STYLE_H2_TEXT={
    'border': '3px solid teal',
    'padding': '20px',
    'border-radius': '10px',
    'text-align': 'center',
    'background-color': 'white',
    'width': '90%',
    'margin':'auto'
}
STYLE_TD={
    'border':'1px solid teal',

}
STYLE_TH={

}

layout = html.Div([
    html.Br(),
    dbc.Row([html.H3("Australia's Emergency Departments Performance by States in 2021-2022")],
            style={'padding-left':'1rem'}),
    html.Hr(),
    dbc.Row([
        html.H5('STATE: ', style={'width': '5rem'}),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': states[i], 'value': i} for i in range(len(states))],
            value=0,
            style=STYLE_DROPDOW
        )
        ], style={'padding-left':'1rem', 
                'display':'flex',
                'align-items': 'center', 
                'justify-content': 'start'}),
    html.Br(),
    dbc.Row([
        html.Div([html.H3([elementB1(0)], id='elementB1'),
                      html.P('Emergency department presentations in 2021-2022')],
                      style=STYLE_),
        html.Div([html.H3([elementB2(0)],id='elementB2'),
                      html.P('of patients were seen on time overrall 2021-2022')],
                      style=STYLE_,),
        html.Div([html.H3([elementB3(0)], id='elementB3'),
                      html.P('of patients were completed within 4 hours in 2021-2022')],
                      style=STYLE_),
        ],style={'display':'flex',
                 'justify-content': 'space-around',
                 }),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Div([dcc.Graph(figure=elementC(0), id='elementC')]),
            html.Br(),
            html.P('Emergency department presentations per 1,000 population', style=STYLE_TITLE_GRAPH),
            html.Hr(),
            html.Div([dcc.Graph(figure=elementD(0),id='elementD')])
        ],width=4),
        dbc.Col([
            html.Br(),
            html.P('Proportion seen on time by triagle category', 
                   style=STYLE_TITLE_GRAPH),
            html.Div(elementE(0), 
                     style ={'display':'block'},
                     id='elementE'),
            html.Br(),
            html.Table([
                html.Tr([
                    html.Th(['Median waiting time in minutes',
                             html.Br(), 
                             '(50% of patient)'],
                             style={'color': 'white','background-color': 'teal','text-align': 'center','border':'1px solid teal', 'width':'50%'}),
                    html.Th(['Waiting time in minutes',
                             html.Br(), 
                             '(90% of patient)'],
                             style={'color': 'white','background-color': 'teal','text-align': 'center','border':'1px solid teal', 'width':'50%'}),
                ]),
                html.Tr([
                    html.Td([dcc.Graph(figure=elementF(0,0),id = 'elementFL')],
                             style={'border':'1px solid teal'}
                            ),
                    html.Td([dcc.Graph(figure=elementF(0,0,False),id = 'elementFR')],
                            style={'border':'1px solid teal'}
                            ),
                ])
            ],style={'margin':'auto'}),
            html.Br(),
            html.P('Emergency Presentations bt triage Category', style=STYLE_TITLE_GRAPH),
            html.Hr(),
            html.Div([dcc.Graph(figure=elementG(0,0),
                                id='elementG')])
        ],width=4),
        dbc.Col([
            html.Br(),
            html.P('PERIOD', style=STYLE_TITLE_GRAPH),
            dcc.Slider(0, 5,1, value=5, 
                       marks={0:'2017',
                              1:'2018',
                              2:'2019',
                              3:'2020',
                              4:'2021',
                              5:'2022'},
                        id='period'),
            html.Hr(),
            html.Div([dcc.Graph(figure=elementH1(0,5),
                                id='elementH1')]),
            html.Br(),
            html.Div([html.H3([elementH2_text(0)], id='elementH2_text',
                              style={'color':'teal'}),
                      html.P('of patients were admitted to hospital from emergency departments with a length of stay less tham equal to 4 hours')],
                      style=STYLE_H2_TEXT),
            html.Br(),
            html.Div([dcc.Graph(figure=elementH2_graph(0,5),
                                id='elementH2_graph')]),
        ],width=4),
    ]),
    html.Br()
])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.layout= layout

@callback(
    [Output(component_id='elementB1', component_property='children'),
    Output(component_id='elementB2', component_property='children'),
    Output(component_id='elementB3', component_property='children'),
    Output(component_id='elementC', component_property='figure'),
    Output(component_id='elementD', component_property='figure'),
    Output(component_id='elementE', component_property='children'),],
    Input(component_id='dropdown', component_property='value')
)
def update_elementBCDE(state_index):
    return elementB1(state_index),elementB2(state_index),elementB3(state_index),elementC(state_index),elementD(state_index),elementE(state_index)
    # return elementB1(state_index),elementB2(state_index),elementB3(state_index),elementD(state_index),elementE(state_index)


@callback(
    [Output(component_id='elementH1', component_property='figure'),
    Output(component_id='elementH2_text', component_property='children'),
    Output(component_id='elementH2_graph', component_property='figure')],
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='period', component_property='value')]
)
def update_elementH(state_index, period):
    if period == 0:
        return elementH1(state_index,1),elementH2_text(state_index),elementH2_graph(state_index,1)
    return elementH1(state_index,period),elementH2_text(state_index),elementH2_graph(state_index,period)

@callback(
    [Output(component_id='elementFL', component_property='figure'),
    Output(component_id='elementFR', component_property='figure'),
    Output(component_id='elementG', component_property='figure')],
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='button_0', component_property='n_clicks'),
    Input(component_id='button_1', component_property='n_clicks'),
    Input(component_id='button_2', component_property='n_clicks'),
    Input(component_id='button_3', component_property='n_clicks'),
    Input(component_id='button_4', component_property='n_clicks'),]
)
def update_elementFG(state_index,btn0,btn1,btn2,btn3,btn4):
    if "button_0" == ctx.triggered_id:
        return elementF(state_index,0,True),elementF(state_index,0,False),elementG(state_index,0)
    elif "button_1" == ctx.triggered_id:
        return elementF(state_index,1,True),elementF(state_index,1,False),elementG(state_index,1)
    elif "button_2" == ctx.triggered_id:
        return elementF(state_index,2,True),elementF(state_index,2,False),elementG(state_index,2)
    elif "button_3" == ctx.triggered_id:
        return elementF(state_index,3,True),elementF(state_index,3,False),elementG(state_index,3)
    elif "button_4" == ctx.triggered_id:
        return elementF(state_index,4,True),elementF(state_index,4,False),elementG(state_index,4)
    else:
        return elementF(state_index,0,True),elementF(state_index,0,False),elementG(state_index,0)

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)