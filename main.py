from dash import  html, dcc
import pandas as pd
import plotly.graph_objects as go

from app import *
import scrap_football
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc

##DATA TREATMENT
def get_month(month_day):
    month_day = str(month_day)

    if "Janeiro" in month_day:
       return 1
    elif "Fevereiro" in month_day:
       return 2
    elif "Março" in month_day:
       return 3
    elif "Abril" in month_day:
       return 4
    elif "Maio" in month_day:
       return 5
    elif "Junho" in month_day:
       return 6
    elif "Julho" in month_day:
       return 7
    elif "Agosto" in month_day:
       return 8
    elif "Setembro" in month_day:
       return 9
    elif "Outubro" in month_day:
       return 10
    elif "Novembro" in month_day:
       return 11
    elif "Dezembro" in month_day:
       return 12

def get_day(str_day):
    dia = str_day.split(',')
    return int(dia[0][-2:].replace(' ', ''))

def data_treatment(df):
    #Convert the date
    df.drop_duplicates(inplace=True)
    df['year'] = pd.to_numeric(df['date'].str[-4:], errors='coerce')
    df['year'] = df['year'].astype('Int64')
    df['month'] = df.apply(lambda x: get_month(x['date']), axis=1)
    df['month'] = df['month'].astype('Int64')
    df['day'] = df.apply(lambda x: get_day(x['date']), axis=1)
    df['day'] = df['day'].astype('Int64')
    df.dropna(inplace=True)
    df['date'] = df.apply(lambda x: datetime.datetime(x['year'], x['month'], x['day']), axis=1)

    return df

df = pd.read_csv('data.csv')
df = data_treatment(df)

button_click = 0

# =========  Layout  =========== #
font_type_size = {'font-family': 'Voltaire', 'font-size': '30px'}
graph_theme = 'simple_white'
font_theme=dict(family="Courier New, monospace",
                size=14,color="#1d428a")

app.layout = dbc.Container(children=[
    #First Row
    dbc.Row([
#Card column
        dbc.Col([
            dbc.Card(
                [
                    html.H2("SOCCER STATS ", style=font_type_size),
                    html.Hr(),

                    #First team dropdown
                    html.H6("Select Team A: "),
                    dcc.Dropdown(
                        df['team_1'].unique(), df['team_1'][0], multi=False, id='team_a_select',

                    ),
                    html.H6("Pitch team A:",style={'margin-top': '8px'}),
                    dcc.RadioItems(['Home', 'Away', 'Both'], 'Both',  id='pitch_A'),

                    #Second team dropdown
                    html.H6("Select Team B: ", style={'margin-top' : '20px'}),
                    dcc.Dropdown(
                        df['team_2'].unique(), df['team_2'][0], multi=False, id='team_b_select'),
                    html.H6("Pitch team B:",style={'margin-top': '8px'}),
                    dcc.RadioItems(['Home', 'Away', 'Both'], 'Both',  id='pitch_B'),

                    html.Hr(style={'margin-top': '40px'}),

                    html.H4("Stats comparsion:",style={'margin-top': '20px'}),

                    html.H6("Corners: ", style={'margin-top': '10px'}),
                    dcc.Input(id="input_corner", type="number", value=2,style={'marginRight':'10px'}),

                    html.H6("Goals: ", style={'margin-top': '10px'}),
                    dcc.Input(id="input_goals", type="number", value=1,style={'marginRight':'10px'}),


                    html.Hr(style={'margin-top': '40px'}),
                    html.H4("Match population:",style={'margin-top': '20px'}),
                    dcc.Slider(0, 50, step=None,
                      marks={
                          1: '1',
                          5: '5',
                          10: '10',
                          20: '15',
                          50: 'All'
                      },
                      value=5,
                      id='slider_match_amount'),

                    html.Hr(style={'margin-top': '40px'}),
                    dbc.Button("Update matches", color="primary", id='update_button',style={'margin-top': '15px'})
                ], style={"margin": "5px", "padding": "20px"})
        ], lg=2),

        #Graphs column
        dbc.Col([
            dbc.Card([
                # First row: will content the graphs of team A
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Col(dcc.Graph(id='goals_team_A',
                                                  config={"displayModeBar": False, "showTips": False})),
                                html.P(id='resume_goals_A')
                            ])
                        ])
                    ], lg=4, sm=12),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Col(dcc.Graph(id='cards_team_A',
                                                  config={"displayModeBar": False, "showTips": False}))
                            ])
                        ])
                    ], lg=4, sm=12),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Col(dcc.Graph(id='corners_team_A',
                                                  config={"displayModeBar": False, "showTips": False})),
                                html.P(id='resume_corners_A')
                            ])
                        ])
                    ], lg=4, sm=12),

                ], style={'margin-top': '20px'}),

                #Third row: will content the graphs of team B
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Col(dcc.Graph(id='goals_team_B',
                                                  config={"displayModeBar": False, "showTips": False})),
                                html.P(id='resume_goals_B')
                            ])
                        ])
                    ], lg=4, sm=12),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Col(dcc.Graph(id='cards_team_B',
                                                  config={"displayModeBar": False, "showTips": False}))
                            ])
                        ])
                    ], lg=4, sm=12),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Col(dcc.Graph(id='corners_team_B',
                                                  config={"displayModeBar": False, "showTips": False})),
                                html.P(id='resume_corners_B')
                            ])
                        ])
                    ], lg=4, sm=12),

                ], style={'margin-top': '20px'})
            ],style={"margin": "5px", "padding": "10px"})
        ], lg=10)
    ])
], style={"padding": "0px"}, fluid=True)

#CALLBACKS
@app.callback(
    [dash.dependencies.Output("goals_team_A", "figure"),
     dash.dependencies.Output("cards_team_A", "figure"),
     dash.dependencies.Output("corners_team_A", "figure"),
     dash.dependencies.Output("goals_team_B", "figure"),
     dash.dependencies.Output("cards_team_B", "figure"),
     dash.dependencies.Output("corners_team_B", "figure"),
     dash.dependencies.Output("resume_goals_A", "children"),
     dash.dependencies.Output("resume_corners_A", "children"),
     dash.dependencies.Output("resume_goals_B", "children"),
     dash.dependencies.Output("resume_corners_B", "children")],
    [dash.dependencies.Input("team_a_select", "value"),
    dash.dependencies.Input("pitch_A", "value"),
    dash.dependencies.Input("team_b_select", "value"),
    dash.dependencies.Input("pitch_B", "value"),
    dash.dependencies.Input("input_corner", "value"),
    dash.dependencies.Input("input_goals", "value"),
    dash.dependencies.Input('slider_match_amount', 'value'),
    dash.dependencies.Input('update_button', 'n_clicks')])

def display_graphs(team_a, pitch_a, team_b, pitch_b, corners, goals, population, n_clicks):
    if(pitch_a != 'Both'):
        if(pitch_a == 'Home'):
            dff_a = df[df['team_1'] == team_a]
            dff_a = dff_a[dff_a['home_away'] == 'home'].tail(population)
        else:
            dff_a = df[df['team_1'] == team_a]
            dff_a = dff_a[dff_a['home_away'] == 'away'].tail(population)
    else:
        dff_a = df[df['team_1'] == team_a].tail(population)

    if (pitch_b != 'Both'):
        if (pitch_b == 'Home'):
            dff_b = df[df['team_1'] == team_b]
            dff_b = dff_b[dff_b['home_away'] == 'home'].tail(population)
        else:
            dff_b = df[df['team_1'] == team_b]
            dff_b = dff_b[dff_b['home_away'] == 'away'].tail(population)
    else:
        dff_b = df[df['team_1'] == team_b].tail(population)

    goals_team_A = px.scatter(dff_a,x='date', y="score_1",
                                title=f'Distribution of goals of {team_a} in the last {population} games')
    goals_team_A.add_trace(go.Line(x=dff_a['date'], y=dff_a['score_2'], marker_color='red', mode='markers', name='adv'))
    goals_team_A.add_trace(go.Line(x=dff_a['date'], y=(len(dff_a['score_1']) * [goals]), name=f'{goals} Gols', marker_color='purple'))
    goals_team_A.update_layout(template=graph_theme,title_x=0.5,font=font_theme, barmode='overlay')

    goals_team_B = px.scatter(dff_b,x='date', y="score_1",
                                title=f'Distribution of goals of {team_b} in the last {population} games')
    goals_team_B.add_trace(go.Line(x=dff_b['date'], y=dff_b['score_2'], marker_color='red', mode='markers', name='adv'))
    goals_team_B.add_trace(go.Line(x=dff_b['date'], y=(len(dff_b['score_1']) * [goals]), name=f'{goals} Gols' ,marker_color='purple'))
    goals_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme, barmode='overlay')

    cards_team_A = px.scatter(dff_a, x='date', y='y_cards_1', title=f'Incidence of n cards of {team_a} in the past {population} games')
    cards_team_A.add_trace(go.Line(x=dff_a['date'],y=dff_a['r_cards_1'],  marker_color='red', mode='markers', name='RED CARD'))
    cards_team_A.update_layout(template=graph_theme, title_x=0.5, font=font_theme)

    cards_team_B = px.scatter(dff_b, x='date', y='y_cards_1',
                           title=f'Incidence of n cards of {team_b} in the past {population} games')
    cards_team_B.add_trace(go.Line(x=dff_b['date'], y=dff_b['r_cards_1'], marker_color='red', mode='markers', name='RED CARD'))
    cards_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme)




    corners_team_A = px.scatter(dff_a, x='date', y="escanteios_1",
                              title=f'Distribution of CORNERS of {team_a} in the last {population} games')
    corners_team_A.add_trace(go.Line(x=dff_a['date'], y=dff_a['escanteios_2'], marker_color='red', mode='markers', name='adv'))
    corners_team_A.add_trace(go.Line(x=dff_a['date'], y=(len(dff_a['escanteios_2']) * [corners]), name=f'{corners} Corners', marker_color='purple'))
    corners_team_A.update_layout(template=graph_theme, title_x=0.5, font=font_theme, barmode='overlay')

    corners_team_B = px.scatter(dff_b, x='date', y="escanteios_1",
                              title=f'Distribution of CORNERS of {team_b} in the last {population} games')
    corners_team_B.add_trace(go.Line(x=dff_b['date'], y=dff_b['escanteios_2'], marker_color='red', mode='markers', name='adv'))
    corners_team_B.add_trace(go.Line(x=dff_b['date'], y=(len(dff_b['escanteios_2']) * [corners]), name=f'{corners} Corners', marker_color='purple'))
    corners_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme, barmode='overlay')

    resume_goals_A = f'{team_a} scored {goals}  goals in {len(dff_a[dff_a["score_1"] >= goals]) / len(dff_a["score_1"]) * 100:.2f}% of the last {population} matches;\'' \
                     f'{team_a} suffered {goals}  goals in {len(dff_a[dff_a["score_2"] >= goals]) / len(dff_a["score_2"]) * 100:.2f}% of the last {population} matches;'

    resume_corners_A = f'{team_a} got {corners}  corners in {len(dff_a[dff_a["escanteios_1"] >= corners]) / len(dff_a["escanteios_1"]) * 100:.2f}% of the last {population} matches;\'' \
                       f'{team_a} suffered {corners}  corners in {len(dff_a[dff_a["escanteios_2"] >= corners]) / len(dff_a["escanteios_2"]) * 100:.2f}% of the last {population} matches;'

    resume_goals_B = f'{team_b} scored {goals}  goals in {len(dff_b[dff_b["score_1"] >= goals]) / len(dff_b["score_1"]) * 100:.2f}% of the last {population} matches;\'' \
                     f'{team_b} suffered {goals}  goals in {len(dff_b[dff_b["score_2"] >= goals]) / len(dff_b["score_2"]) * 100:.2f}% of the last {population} matches;'

    resume_corners_B = f'{team_b} got {corners}  corners in {len(dff_b[dff_b["escanteios_1"] >= corners]) / len(dff_b["escanteios_1"]) * 100:.2f}% of the last {population} matches;\'' \
                       f'{team_b} suffered {corners}  corners in {len(dff_b[dff_b["escanteios_2"] >= corners]) / len(dff_b["escanteios_2"]) * 100:.2f}% of the last {population} matches;'

    global button_click
    if(n_clicks is None):
        print("")
    else:
        if(n_clicks == button_click):
            print('')
        else:
            print('downloading')
            button_click = n_clicks
            scrap_football.update_csv_matches()

    return goals_team_A, cards_team_A, corners_team_A,\
           goals_team_B, cards_team_B, corners_team_B, \
           resume_goals_A, resume_corners_A, \
           resume_goals_B, resume_corners_B

#EXECUTE
if __name__ == '__main__':
    app.run_server(debug=True)