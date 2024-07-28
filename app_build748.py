import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data
data = pd.read_csv('MyTcas.csv') + pd.read_csv('university_logos.csv') 

# Ensure that the admission columns are numeric
admission_columns = ["Portfolio", "Quota", "Admission", "Direct Admission"]
for col in admission_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

# Create map figure with university logo and name
map_fig = px.scatter_mapbox(
    data,
    lat="Latitude",
    lon="Longitude",
    hover_name="ชื่อมหาลัย",
    hover_data={"Logo_URL": True, "Latitude": False, "Longitude": False},
    size="Admission",
    color="Admission",
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=30,
    zoom=5,
    mapbox_style="carto-positron",
    height=500
)

# Create bar chart for admission rounds
bar_fig = px.bar(
    data,
    x="ชื่อมหาลัย",
    y=admission_columns,
    barmode='group',
    labels={"value": "จำนวน", "variable": "รอบการสมัคร"},
    title="จำนวนที่รับสมัครในรอบต่างๆ"
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        "แดชบอร์ดการรับสมัครเข้าคณะวิศวะ",
        style={
            'textAlign': 'center',
            'color': '#ffffff',
            'font-family': 'Arial, sans-serif',
            'padding': '20px',
            'backgroundColor': '#1c1c1c'
        }
    ),

    html.H2(
        "แผนที่แสดงตำแหน่งมหาวิทยาลัยและข้อมูลการรับสมัคร",
        style={
            'textAlign': 'center',
            'color': '#ffffff',
            'font-family': 'Arial, sans-serif',
            'padding': '10px',
            'backgroundColor': '#333333'
        }
    ),
    
    dcc.Graph(
        id='map',
        figure=map_fig,
        style={'height': '150vh', 'width': '100%'}
    ),
    
    html.Div([
        html.Label(
            "เลือกมหาวิทยาลัย:",
            style={'font-family': 'Arial, sans-serif', 'font-size': '18px', 'padding': '10px', 'color': '#ffffff'}
        ),
        dcc.Dropdown(
            id='university-dropdown',
            options=[{'label': uni, 'value': uni} for uni in data['ชื่อมหาลัย'].unique()],
            value=[],
            multi=True,
            style={'font-family': 'Arial, sans-serif', 'width': '50%', 'margin': 'auto', 'color': '#1c1c1c'}
        )
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#333333'}),
    
    dcc.Graph(
        id='bar',
        figure=bar_fig,
        style={'height': '70vh', 'width': '100%'}
    ),
    
    html.Div([
        html.H3(
            "รายละเอียดมหาวิทยาลัย",
            style={
                'textAlign': 'center',
                'color': '#ffffff',
                'font-family': 'Arial, sans-serif',
                'padding': '10px',
                'backgroundColor': '#333333'
            }
        ),
        dcc.Graph(id='table', style={'height': '70vh', 'width': '100%'})
    ], style={'backgroundColor': '#1c1c1c', 'padding': '20px'})
], style={'backgroundColor': '#1c1c1c'})

@app.callback(
    [Output('bar', 'figure'),
     Output('table', 'figure')],
    [Input('university-dropdown', 'value')]
)
def update_charts(selected_universities):
    if not selected_universities:
        filtered_data = data
    else:
        filtered_data = data[data['ชื่อมหาลัย'].isin(selected_universities)]
    
    new_bar_fig = px.bar(
        filtered_data,
        x="ชื่อมหาลัย",
        y=admission_columns,
        barmode='group',
        labels={"value": "จำนวน", "variable": "รอบการสมัคร"},
        title="จำนวนที่รับสมัครในรอบต่างๆ"
    )
    
    table_fig = go.Figure(
        data=[go.Table(
            header=dict(values=list(filtered_data.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[filtered_data[col] for col in filtered_data.columns],
                       fill_color='lavender',
                       align='left')
        )]
    )
    
    return new_bar_fig, table_fig

if __name__ == '__main__':
    app.run_server(debug=True)
