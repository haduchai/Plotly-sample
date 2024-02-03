
import pandas as pd
import json
import geopandas as gpd
import geoplot as gplt
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html,dcc
from plotly.subplots import make_subplots
import plotly.express as px
from urllib.request import urlopen

# đọc file excel
df_B = pd.read_excel('data.xlsx', sheet_name='ElementB')
df_males = pd.read_excel('data.xlsx', sheet_name='Males_age')
df_females = pd.read_excel('data.xlsx', sheet_name='Females_age')
df_E = pd.read_excel('data.xlsx', sheet_name='ElementE')
df_F_mean = pd.read_excel('data.xlsx', sheet_name='ElementF_median')
df_F_90 = pd.read_excel('data.xlsx', sheet_name='ElementF_90')
df_G = pd.read_excel('data.xlsx', sheet_name='ElementG')
df_H1 = pd.read_excel('data.xlsx', sheet_name='ElementH1', index_col=0)
df_H1 = df_H1.T
df_H1.reset_index(inplace=True)
df_H2 = pd.read_excel('data.xlsx', sheet_name='ElementH2', index_col=0)
df_H2 = df_H2.T
df_H2.reset_index(inplace=True)

"""
--------------------------------Element B--------------------------------
"""


states = df_B['states'].tolist()
E_present = df_B['E_present'].tolist()
E_present_seen_on_time = df_B['E_present_seen_on_time'].tolist()
E_4hours_less = df_B['E_4hours_less'].tolist()

def elementB1(state_index):
    return f'{E_present[state_index]}'
def elementB2(state_index):
    return f'{E_present_seen_on_time[state_index]} %'
def elementB3(state_index):
    return f'{E_4hours_less[state_index]} %'


"""
--------------------------------Element C--------------------------------
"""
# Geojson
# with urlopen('states.geojson') as response:
json_data = gpd.read_file('states.geojson')
colors = [0]*8

# tạo dataframe với states và color kèm id
ids = list(range(1, len(states) + 1))

# Tạo DataFrame
data = {
    'id': ids,
    'states': states,
    'color': colors
}
df = pd.DataFrame(data)
def elementC(index):
    color = ['None']*8
    color[index] = 'teal'

    fig = px.choropleth_mapbox(
        data_frame = df,            # Data frame with values
        geojson = json_data,                      # Geojson with geometries
        featureidkey = 'properties.STATE_NAME', # Geojson key which relates the file with the data from the data frame
        locations = 'states',
        range_color = [0, 1],          # Range of the colorbar
        color=color,  
        color_discrete_map = {'teal':'teal', 'None':'white'},
        mapbox_style = 'white-bg',
        center = dict(lat = -25.2744, lon = 133.7751),
        zoom = 2)
    
    # Hide the color label in the figure
    fig.update_layout(showlegend=False)
    return fig

"""
--------------------------------Element D--------------------------------
"""
categories = df_males['Category'].tolist()
df_males.drop(columns=['Category'], inplace=True)
df_females.drop(columns=['Category'], inplace=True)
males = df_males.values
females = df_females.values

females = [[-item for item in row] for row in females]

def elementD(state_index):
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
    # bar plot for females
    fig.append_trace(go.Bar(x=females[state_index], y=categories,
                            orientation='h', 
                            name='Females',
                            marker=dict(color='teal'),
                            meta = [-i for i in females[state_index]],
                            hovertemplate='Age group: <b>%{y} years old</b><br>Females: <b>%{meta} presentations per 1,000 population</b>'),
                            1,1)
    # bar plot for males
    fig.append_trace(go.Bar(x=males[state_index], y=categories,
                            orientation='h',
                            name='Males', 
                            marker=dict(color='#00B0B0'),
                            hovertemplate='Age group: <b>%{y} years old</b><br>Males: <b>%{x} presentations per 1,000 population</b>'),
                            1, 2)
    fig.update_xaxes(showgrid=False, showline =True, visible=False)
    fig.update_yaxes(showgrid=False, showline=False)
    fig.update_layout(xaxis=dict(visible=False),
                      margin=dict(t=0, b=0, l=0, r=0),
                    barmode='relative',
                    legend=dict(orientation="h", yanchor="bottom",
                                y=1, xanchor="center", x=0.5),
                    plot_bgcolor='#ffffff')
    return fig 


"""
--------------------------------Element E--------------------------------
"""
STYLE_BUTTON={
    'width':'100%',
    'height':'40px',
    'opacity':0,
    'border':'none',
}
hospitals = df_E.iloc[:,0].values
time = [10,10,30,90,120]
dataF= df_E.iloc[:,1:]
def row_table(hospital_name,value,id):
    return dbc.Row([
        html.Div([
            html.P(hospital_name, style={'margin':0,'width':'25%'}),
            html.Div([dmc.Progress(value=value, color="Teal",size='xl', radius='xl')],
                 style={'width':'60%'}),
            html.P(f'{value}%', style={'margin':0,'width':'15%', 'text-align':'right'})],
            style={'display':'flex',
                     'align-items': 'center',
                     'position':'absolute',
                     'top':0,
                     'width':'100%',
                     'margin':'auto',
                     'height':'40px'}),
        dbc.Button(style=STYLE_BUTTON,
                    id=f'button_{id}', 
                    n_clicks=0
                    ),
        dbc.Tooltip([html.P(f'{hospital_name} triage category'),
        html.P(f'The triage response time is {time[id]}'),
        html.P(f'{value}% were seen on time')],
                    target=f'button_{id}',
                    placement='right',
                    style={'border': '1px solid black',
                    'border-radius': '10px',
                    'text-align': 'center',
                    'color': '#ffffff'})
        ],style={'position':'relative'},
        )

def hover_text(state_index,select):

    return 

def elementE(state_index):
    layout=[]
    for i in range(5):
        layout.append(row_table(hospitals[i],dataF.iloc[i,state_index],i))
    return layout
# html.Div(elementE(2),style ={'display':'block'})


"""
--------------------------------Element F--------------------------------
"""
dataF_mean = df_F_mean.iloc[:,1:]
dataF_90 = df_F_90.iloc[:,1:]

def elementF(state_index,select,mean=True):
    # print(select)
    colors = ['lightslategray','lightgray','gray','dimgray','darkgray']
    colors[select]='purple'
    hospitals = ['Resuscitation','Emergency','Urgent','Semi-urgent','Non-urgent']
    data = pd.DataFrame({'hospitals': hospitals,'colors':colors})
    if mean:
        data['time']=dataF_mean.iloc[:,state_index]
    else:
        data['time']=dataF_90.iloc[:,state_index]
        data = data.sort_values(by='time',ascending=False).reset_index(drop = True)
    fig = go.Figure(data=[go.Scatter(x=[-4.5,5.5,1,1,-5.5],
                                 y=[0,0,-7.2,6.5,8],
                                 mode='markers+text',
                                 marker=dict(size=[100,90,80,70,60],
                                             color = data.colors),
                                 text=[f'<b>{data.hospitals[i]}<b><br>{data.time[i]} minutes' for i in range(5)],
                                 textposition='middle center',
                                 textfont=dict(size=10)
                                 )],
                layout=go.Layout(yaxis=dict(scaleanchor="x", 
                                            scaleratio=1, 
                                            range=[-10, 10],
                                            visible=False,
                                            ),
                                 xaxis=dict(range=[-10,10]
                                            ,visible=False
                                            ),
                                 width=200, 
                                 height=250,
                                 margin = dict(l=0, r=0, b=0, t=0),
                                 template = "none"
                                 ))
    return fig


"""
--------------------------------Element G--------------------------------
"""
dataG = df_G.iloc[:,1:]
def elementG(state_index,select):
  colors = ['lightslategray','lightgray','gray','dimgray','darkgray']
  colors[select]='purple'
  values = dataG.iloc[:,state_index].values
  fig = go.Figure(
      data=[go.Pie(labels=hospitals, 
                  values=values, 
                  hole=.3,
                  marker_colors=colors,
                  textinfo='label + value + percent',
                  textposition='outside'
                  )],
      layout=go.Layout( showlegend=False,margin = dict(l=0, r=0, b=0, t=0))
  )
  return fig



"""
--------------------------------Element H--------------------------------
"""
dataH1 = df_H1.iloc[:,1:]
period = df_H1['index'].to_list()[1:]
print(dataH1)

dataH2 = df_H2.iloc[:,1:]
print(dataH2)


# dataH1 = pd.DataFrame({
#     'New South Wales':[73.5,71.7,71.3,69.0,64.2], 
#     'Victoria':[69.2,67.5,64.9,62.0,55.3], 
#     'Queensland':[72.1,70.2,70.8,69.1,61.4], 
#     'Western Australia':[75.7,74.9,75.4,70.7,64.6], 
#     'South Australia':[60.8,59.4,62.4,60.8,57.6], 
#     'Tasmania':[64.4,62.0,60.0,57.7,55.2], 
#     'Australian Capital Territory':[64.0,59.5,57.6,56.6,52.4], 
#     'Northern Territory':[62.7,66.8,67.1,63.6,58.8]
# })
# period = ['2017–18','2018-19','2019-20','2020–21','2021–22']

# dataH2 = pd.DataFrame({
#     'New South Wales':[43.2,40.8,40.0,35.8,28.7],
#     'Victoria':[52.9,51.0,48.2,44.6,36.9],
#     'Queensland':[54.8,53.3,54.3,48.5,39.0],
#     'Western Australia':[53.8,50.9,52.1,42.6,34.0],
#     'South Australia':[40.8,40.2,43.3,42.2,39.1],
#     'Tasmania':[28.2,27.5,26.7,23.3,24.5],
#     'Australian Capital Territory':[40.3,34.5,34.9,37.7,33.0],
#     'Northern Territory':[31.3,35.4,35.6,32.1,27.4]
# })

def elementH1(state_index, period_value):
  fig = go.Figure(
      data=[
          go.Bar(
              y = [90]*(period_value),
              x = period[:period_value],
              marker=dict(color='teal'),
              text=[90]*(period_value),
              textposition='outside',
              textfont=dict(size=15),
          ),
          go.Scatter(
              x=period[:period_value],
              y=dataH1.iloc[:period_value,state_index],
              mode = 'markers + lines + text',
              text = [f'<b>{i}<b>' for i in  dataH1.iloc[:period_value,state_index]],
              textposition='bottom center',
              marker = dict(size=20, color = 'aqua' ),
              line=dict(color='aqua',width=5),
              textfont=dict(size=15, color='white')
      )],
      layout=go.Layout(yaxis=dict(range=[0,110],
                                  visible=True,
                                  scaleanchor='x',
                                  scaleratio=2),
                      margin = dict(l=0, r=0, b=0, t=0),
                      showlegend=False,
                      plot_bgcolor='white',
                      height=350
      )
  )
  return fig

def elementH2_text(state_index):
  return f'{dataH2.iloc[-1,state_index]}%'
# print(elementH2_text(2))

def elementH2_graph(state_index, period_value):
#   print(dataH2.iloc[:period_value,state_index])
  fig = go.Figure(
      data=[
          go.Scatter(
              x=period[:period_value],
              y=dataH2.iloc[:period_value,state_index],
              mode = 'markers + lines + text',
              text = [f'<b>{i}<b>' for i in dataH2.iloc[:period_value,state_index]],
              textposition='bottom center',
              marker = dict(size=15, color = 'aqua' ),
              line=dict(color='aqua',width=3),
              textfont=dict(size=15, color='black')
      )],
      layout=go.Layout(yaxis=dict(range=[0,70],visible=True),
                      margin = dict(l=0, r=0, b=0, t=0),
                      showlegend=False,
                      plot_bgcolor='white' ,
                      height=350
      )
  )
  return fig
