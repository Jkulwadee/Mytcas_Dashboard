import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('MyTcas.csv')

# Create a numerical DataFrame and an original text DataFrame
numerical_df = df.copy()

# Convert non-numerical data in the relevant columns to 0 for numerical DataFrame
for col in ['Portfolio', 'Quota', 'Admission', 'Direct Admission']:
    numerical_df[col] = pd.to_numeric(numerical_df[col], errors='coerce').fillna(0)

# Calculate totals for Portfolio, Quota, Admission, and Direct Admission
totals = numerical_df[['Portfolio', 'Quota', 'Admission', 'Direct Admission']].sum()

# Create the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.Header([
        html.H1(
            "University Dashboard",
            style={
                'textAlign': 'center',
                'color': '#ffffff',
                'font-family': 'Arial, sans-serif',
                'padding': '30px',
                'backgroundColor': '#210535',
                'margin': '0'
            }
        ),
    ], style={'backgroundColor': '#210535', 'padding-left': '30px'}),

    html.Div([
        html.Label(
            "เลือกมหาวิทยาลัย:",
            style={
                'font-family': 'Arial, sans-serif',
                'font-size': '18px',
                'padding': '10px',
                'color': '#ffffff',
                'display': 'block',
                'text-align': 'left',
                'margin-left': '20px'
            }
        
        ),
        dcc.Dropdown(
            id='university-dropdown',
            options=[{'label': uni, 'value': uni} for uni in df['ชื่อมหาลัย'].unique()],
            placeholder="Select a university",
            style={
                'font-family': 'Arial, sans-serif',
                'width': '80%',
                'margin': 'auto',
                'color': '#000000',
                'backgroundColor': '#ffffff',
                'border': '1px solid #210535',
                'borderRadius': '5px'
            }
        ),
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#210535', 'margin-bottom': '20px'}),

    html.Div([
        html.Label(
            "เลือกสาขา:",
            style={
                'font-family': 'Arial, sans-serif',
                'font-size': '18px',
                'padding': '10px',
                'color': '#ffffff',
                'display': 'block',
                'text-align': 'left',
                'margin-left': '20px'
            }
        ),
        dcc.Dropdown(
            id='course-dropdown',
            placeholder="Select a course",
            style={
                'font-family': 'Arial, sans-serif',
                'width': '80%',
                'margin': 'auto',
                'color': '#000000',
                'backgroundColor': '#ffffff',
                'border': '1px solid #210535',
                'borderRadius': '5px'
            }
        ),
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#210535', 'margin-bottom': '20px'}),

    html.Div([
        dcc.Graph(id='map')
    ], style={'padding': '30px', 'backgroundColor': '#1E0E2C', 'margin-bottom': '30px', 'width': '90%'}),

    html.Div(id='university-details', style={'color': '#ffffff', 'padding': '20px', 'backgroundColor': '#1E0E2C', 'margin-bottom': '20px'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='pie-chart', style={'display': 'inline-block', 'width': '49%'}),
            dcc.Graph(id='bar-chart', style={'display': 'inline-block', 'width': '49%'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'})
    ], style={'padding': '20px', 'backgroundColor': '#1E0E2C', 'margin-bottom': '20px'}),

    html.Div([
        html.H2("University Data Table", style={'textAlign': 'center', 'color': '#ffffff'}),
        dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in df.columns if i not in ['ชื่อมหาลัย','Latitude', 'Longitude']],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'backgroundColor': '#210535', 'color': '#ffffff'},
            style_header={'backgroundColor': '#341259', 'fontWeight': 'bold'},
        )
    ], style={
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': 'auto',
        'border': '1px solid #210535',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.5)',
        'backgroundColor': '#1E0E2C'
    })
], style={'backgroundColor': '#1E0E2C', 'font-family': 'Arial, sans-serif', 'padding': '20px'})

@app.callback(
    Output('course-dropdown', 'options'),
    Input('university-dropdown', 'value')
)
def set_course_options(selected_uni):
    if selected_uni:
        filtered_df = df[df['ชื่อมหาลัย'] == selected_uni]
        return [{'label': course, 'value': course} for course in filtered_df['หลักสูตร'].unique()]
    else:
        return []

@app.callback(
    [Output('map', 'figure'),
     Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('data-table', 'data'),
     Output('university-details', 'children')],
    [Input('university-dropdown', 'value'),
     Input('course-dropdown', 'value')]
)
def update_dashboard(selected_uni, selected_course):
    filtered_df = df
    filtered_numerical_df = numerical_df
    if selected_uni:
        filtered_df = filtered_df[filtered_df['ชื่อมหาลัย'] == selected_uni]
        filtered_numerical_df = filtered_numerical_df[filtered_numerical_df['ชื่อมหาลัย'] == selected_uni]
    if selected_course:
        filtered_df = filtered_df[filtered_df['หลักสูตร'] == selected_course]
        filtered_numerical_df = filtered_numerical_df[filtered_numerical_df['หลักสูตร'] == selected_course]

    # Remove duplicate entries based on 'ชื่อมหาลัย', 'หลักสูตร', 'วิทยาเขต', 'Latitude', and 'Longitude'
    filtered_df = filtered_df.drop_duplicates(subset=['ชื่อมหาลัย', 'หลักสูตร', 'วิทยาเขต', 'Latitude', 'Longitude'])

    if filtered_df.empty:
        # Show a message and the totals when no university is selected
        map_fig = px.scatter_mapbox(
            lat=[0], lon=[0], hover_name=["Please Enter Information"],
            zoom=1, height=750
        )
        map_fig.update_layout(mapbox_style="carto-positron")  # Change the map style
        map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        pie_fig = px.pie(
            names=['Portfolio', 'Quota', 'Admission', 'Direct Admission'],
            values=[totals['Portfolio'], totals['Quota'], totals['Admission'], totals['Direct Admission']],
            title="Total Admission Types"
        )

        bar_fig = px.bar(
            x=['Portfolio', 'Quota', 'Admission', 'Direct Admission'],
            y=[totals['Portfolio'], totals['Quota'], totals['Admission'], totals['Direct Admission']],
            title="Total Admission Types"
        )

        data = []
        university_details = html.Div("Please Enter Information", style={'color': '#ffffff'})

    else:
        # Update the map with different colors and smaller size
        map_fig = px.scatter_mapbox(
            filtered_df, lat="Latitude", lon="Longitude", hover_name="ชื่อมหาลัย",
            hover_data={"ชื่อมหาลัย": False, "วิทยาเขต": True, "Latitude": False, "Longitude": False},
            color="ชื่อมหาลัย", color_continuous_scale=px.colors.cyclical.IceFire,
            zoom=5, height=750, size_max=10, size=[5]*len(filtered_df),
            center={"lat": 13.736717, "lon": 100.523186}  # Center the map on Thailand
        )
        map_fig.update_layout(mapbox_style="carto-positron")  # Change the map style
        map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#1E0E2C', font_color='#ffffff')

        # Update the pie chart to show the distribution of admission types for the selected course
        if not filtered_numerical_df.empty:
            admission_types = filtered_numerical_df[['Portfolio', 'Quota', 'Admission', 'Direct Admission']].sum()
            original_labels = df[['Portfolio', 'Quota', 'Admission', 'Direct Admission']].iloc[0]
            pie_labels = [f"{label}" for label, value in original_labels.items() if admission_types[label] != 0]
            pie_values = [value for value in admission_types.values if value != 0]
            pie_fig = px.pie(
                names=pie_labels, values=pie_values, 
                title=f"Distribution of Admission Types for {selected_course}" if selected_course else "Distribution of Admission Types"
            )
        else:
            pie_fig = px.pie(title="No data available")

        pie_fig.update_layout(paper_bgcolor='#1E0E2C', font_color='#ffffff')
        pie_fig.update_traces(marker=dict(line=dict(width=2, color='black')))

        # Update the bar chart using the same data as the pie chart
        if pie_values:
            bar_fig = px.bar(x=pie_labels, y=pie_values, color=pie_labels, 
                             title="Distribution of Admission Types")
        else:
            bar_fig = px.bar(title="No data available")

        bar_fig.update_layout(paper_bgcolor='#1E0E2C', font_color='#ffffff')
        bar_fig.update_traces(marker=dict(line=dict(width=2, color='black')))

        # Update the table
        data = filtered_df.drop(columns=['Latitude', 'Longitude']).to_dict('records')

        # Update the university details
        if not filtered_df.empty:
            details = filtered_df.to_dict('records')[0]
            detail_items = [html.P(f"{key}: {value}") for key, value in details.items()]
            university_details = html.Div(detail_items, style={'color': '#ffffff'})
        else:
            university_details = html.Div("No details available", style={'color': '#ffffff'})

    return map_fig, pie_fig, bar_fig, data, university_details

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
