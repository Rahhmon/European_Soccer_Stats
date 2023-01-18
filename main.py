import dash.dependencies
from dash import  html, dcc
import pandas as pd
import plotly.graph_objects as go
import dash_daq as daq
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
                size=12,color="#1d428a")

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

                    html.H6("Cards: ", style={'margin-top': '10px'}),
                    dcc.Input(id="input_cards", type="number", value=1,style={'marginRight':'10px'}),

                    html.H6("Switch view: ", style={'margin-top': '10px'}),
                    daq.BooleanSwitch(id="swtich_view", on=False, color="dark-blue", style={'margin-top': '10px'}),

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
                                                  config={"displayModeBar": False, "showTips": False})),
                                html.P(id='resume_cards_A')
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
                                                  config={"displayModeBar": False, "showTips": False})),
                                html.P(id='resume_cards_B')
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
], style={"padding": "5px"}, fluid=True)

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
     dash.dependencies.Output("resume_corners_B", "children"),
     dash.dependencies.Output("resume_cards_A", "children"),
     dash.dependencies.Output("resume_cards_B", "children")],
    [dash.dependencies.Input("team_a_select", "value"),
    dash.dependencies.Input("pitch_A", "value"),
    dash.dependencies.Input("team_b_select", "value"),
    dash.dependencies.Input("pitch_B", "value"),
    dash.dependencies.Input("input_corner", "value"),
    dash.dependencies.Input("input_goals", "value"),
    dash.dependencies.Input('slider_match_amount', 'value'),
    dash.dependencies.Input('update_button', 'n_clicks'),
    dash.dependencies.Input('input_cards', 'value'),
     dash.dependencies.Input('swtich_view', 'on')])

def display_graphs(team_a, pitch_a, team_b, pitch_b, corners, goals, population, n_clicks, cards, view_button):
    #Defines the population of each team, according to the selected and matches played
    pop_b = population
    pop_a = population
    if(pitch_a != 'Both'):
        if(pitch_a == 'Home'):
            dff_a = df[df['team_1'] == team_a]
            pop_a = len(dff_a[dff_a['home_away'] == 'home'].tail(population))
            dff_a = dff_a[dff_a['home_away'] == 'home'].tail(pop_a)
        else:
            dff_a = df[df['team_1'] == team_a]
            pop_a = len(dff_a[dff_a['home_away'] == 'away'].tail(population))
            dff_a = dff_a[dff_a['home_away'] == 'away'].tail(pop_a)
    else:
        pop_a = len(df[df['team_1'] == team_a].tail(population))
        dff_a = df[df['team_1'] == team_a].tail(pop_a)

    if (pitch_b != 'Both'):
        if (pitch_b == 'Home'):
            dff_b = df[df['team_1'] == team_b]
            pop_b = len(dff_b[dff_b['home_away'] == 'home'].tail(population))
            dff_b = dff_b[dff_b['home_away'] == 'home'].tail(pop_b)
        else:
            dff_b = df[df['team_1'] == team_b]
            pop_b = len(dff_b[dff_b['home_away'] == 'away'].tail(population))
            dff_b = dff_b[dff_b['home_away'] == 'away'].tail(pop_b)
    else:
        pop_b = len(df[df['team_1'] == team_b].tail(population))
        dff_b = df[df['team_1'] == team_b].tail(pop_a)

    if(not view_button):
        #Plots the first graph: N_Goals occurence of Team_A
        goals_team_A = px.line(dff_a, x='date', y=len(dff_a['score_1']) * [goals],
                               title=f'Goals of {team_a} in the last {pop_a} games')
        goals_team_A.add_trace(go.Line(x= dff_a['date'], y=dff_a["score_1"], marker_color='green', mode='markers', name=f'{team_a}'))
        goals_team_A.add_trace(go.Line(x=dff_a['date'], y=dff_a['score_2'], marker_color='red', mode='markers', name='adv'))
        goals_team_A.update_layout(template=graph_theme,title_x=0.5,font=font_theme,
                                           xaxis={'visible': False, 'showticklabels': False}, yaxis_title = '')

        goals_team_B = px.line(dff_b, x='date', y=len(dff_b['score_1']) * [goals],
                               title=f'Goals of {team_b} in the last {pop_b} games')
        goals_team_B.add_trace(
            go.Line(x=dff_b['date'], y=dff_b["score_1"], marker_color='green', mode='markers', name=f'{team_b}'))
        goals_team_B.add_trace(go.Line(x=dff_b['date'], y=dff_b['score_2'], marker_color='red', mode='markers', name='adv'))
        goals_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis={'visible': False, 'showticklabels': False}, yaxis_title='')

        cards_team_A = px.line(dff_a, x='date', y=len(dff_a['y_cards_1']) * [cards],
                               title=f'Cards of {team_a} in the last {pop_a} games')
        cards_team_A.add_trace(
            go.Line(x=dff_a['date'], y=dff_a["y_cards_1"], marker_color='#ffcc00', mode='markers', name='Y_CARDS'))
        cards_team_A.add_trace(go.Line(x=dff_a['date'], y=dff_a['r_cards_1'], marker_color='red', mode='markers', name='R_CARDS'))
        cards_team_A.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis={'visible': False, 'showticklabels': False}, yaxis_title='')


        cards_team_B = px.line(dff_b, x='date', y=len(dff_b['y_cards_1']) * [cards],
                               title=f'Cards of {team_b} in the last {pop_b} games')
        cards_team_B.add_trace(
            go.Line(x=dff_b['date'], y=dff_b["y_cards_1"], marker_color='#ffcc00', mode='markers', name='Y_CARDS'))
        cards_team_B.add_trace(
            go.Line(x=dff_b['date'], y=dff_b['r_cards_1'], marker_color='red', mode='markers', name='R_CARDS'))
        cards_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis={'visible': False, 'showticklabels': False}, yaxis_title='')

        corners_team_A = px.line(dff_a, x='date', y=len(dff_a['escanteios_1']) * [corners],
                               title=f'Corners of {team_a} in the last {pop_a} games')
        corners_team_A.add_trace(
            go.Line(x=dff_a['date'], y=dff_a["escanteios_1"], marker_color='green', mode='markers', name=f'{team_a}'))
        corners_team_A.add_trace(go.Line(x=dff_a['date'], y=dff_a['escanteios_2'], marker_color='red', mode='markers', name='adv'))
        corners_team_A.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis={'visible': False, 'showticklabels': False}, yaxis_title='')

        corners_team_B = px.line(dff_b, x='date', y=len(dff_b['escanteios_1']) * [corners],
                                 title=f'Corners of {team_b} in the last {pop_b} games')
        corners_team_B.add_trace(
            go.Line(x=dff_b['date'], y=dff_b["escanteios_1"], marker_color='green', mode='markers', name=f'{team_b}'))
        corners_team_B.add_trace(
            go.Line(x=dff_b['date'], y=dff_b['escanteios_2'], marker_color='red', mode='markers', name='adv'))
        corners_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                     xaxis={'visible': False, 'showticklabels': False}, yaxis_title='')
    else:
        goals_team_A = px.histogram(dff_a, x='score_1', title=f'Goals of {team_a} in the last {pop_a} games')
        goals_team_A.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis_title='', yaxis_title='')

        cards_team_A = px.histogram(dff_b, x='y_cards_1', title=f'Cards of {team_a} in the last {pop_a} games')
        cards_team_A.add_trace(go.Histogram(x=dff_a['r_cards_1'], name='red_card',marker_color ='red'))
        cards_team_A.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis_title='', yaxis_title='', barmode='stack')

        corners_team_A = px.histogram(dff_a, x='escanteios_1', title=f'Corners of {team_a} in the last {pop_a} games')
        corners_team_A.add_trace(go.Histogram(x=dff_a['escanteios_2'], name='adv', marker_color='red'))
        corners_team_A.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis_title='', yaxis_title='')

        goals_team_B = px.histogram(dff_b, x='score_1', title=f'Goals of {team_b} in the last {pop_b} games')
        goals_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                     xaxis_title='', yaxis_title='')

        cards_team_B = px.histogram(dff_a, x='y_cards_1', title=f'Cards of {team_b} in the last {pop_b} games')
        cards_team_B.add_trace(go.Histogram(x=dff_b['r_cards_1'], name='red_card', marker_color='red'))
        cards_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                   xaxis_title='', yaxis_title='', barmode='stack')

        corners_team_B =px.histogram(dff_b, x='escanteios_1', title=f'Corners of {team_b} in the last {pop_b} games')
        corners_team_B.add_trace(go.Histogram(x=dff_b['escanteios_2'], name='adv', marker_color='red'))
        corners_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme,
                                     xaxis_title='', yaxis_title='')

    frequency_A_score = len(dff_a[dff_a["score_1"] >= goals]) / len(dff_a["score_1"])
    frequency_A_get_scored = len(dff_a[dff_a["score_2"] >= goals]) / len(dff_a["score_2"])
    frequency_B_score = len(dff_b[dff_b["score_1"] >= goals]) / len(dff_b["score_1"])
    frequency_B_get_scored = len(dff_b[dff_b["score_2"] >= goals]) / len(dff_b["score_2"])
    freq_prob_A_scores_B = frequency_A_score * frequency_B_get_scored
    freq_prob_B_scores_A = frequency_B_score * frequency_A_get_scored
    resume_goals_A = f'{team_a} scored {goals}  goals in {frequency_A_score*100:.2f}% of the last {pop_a} matches;\'' \
                     f'{team_a} suffered {goals}  goals in {frequency_A_get_scored*100:.2f}% of the last {pop_a} matches;' \
                     f'Probability of {team_a} makes {goals} goal is: {freq_prob_A_scores_B*100:.2f}%'
    resume_goals_B = f'{team_b} scored {goals}  goals in {frequency_B_score*100:.2f}% of the last {pop_b} matches;\'' \
                     f'{team_b} suffered {goals}  goals in {frequency_B_get_scored*100:.2f}% of the last {pop_b} matches;' \
                     f'Probability of {team_b} makes {goals} goal is: {freq_prob_B_scores_A*100:.2f}%'

    frequency_A_corners = len(dff_a[dff_a["escanteios_1"] >= corners]) / len(dff_a["escanteios_1"])
    frequency_A_adv_corners = len(dff_a[dff_a["escanteios_2"] >= corners]) / len(dff_a["escanteios_2"])
    frequency_B_corners = len(dff_b[dff_b["escanteios_1"] >= corners]) / len(dff_b["escanteios_1"])
    frequency_B_adv_corners = len(dff_b[dff_b["escanteios_2"] >= corners]) / len(dff_b["escanteios_2"])
    freq_prob_A_corners_B = frequency_A_corners * frequency_B_adv_corners
    freq_prob_B_corners_A = frequency_B_corners * frequency_A_adv_corners

    resume_corners_A = f'{team_a} got {corners}  corners in {frequency_A_corners * 100:.2f}% of the last {pop_a} matches;\'' \
                       f'{team_b} suffered {corners}  corners in { frequency_A_adv_corners * 100:.2f}% of the last {pop_b} matches;' \
                       f'Probability of {team_a} makes {corners} corners is: {freq_prob_A_corners_B*100:.2f}%'

    resume_corners_B = f'{team_b} got {corners}  corners in { frequency_B_corners* 100:.2f}% of the last {pop_b} matches;\'' \
                       f'{team_a} suffered {corners}  corners in { frequency_B_adv_corners * 100:.2f}% of the last {pop_b} matches;' \
                       f'Probability of {team_b} makes {corners} corners is: {freq_prob_B_corners_A*100:.2f}%'

    resume_cards_A = f'{team_a} got {cards}  Yellow Cards in {len(dff_a[dff_a["y_cards_1"] >= cards]) / len(dff_a["y_cards_1"]) * 100:.2f}% of the last {pop_a} matches;\'' \
                       f'{team_a} got {cards}  Red Cards in {len(dff_a[dff_a["r_cards_1"] >= cards]) / len(dff_a["r_cards_1"]) * 100:.2f}% of the last {pop_a} matches;\'' \

    resume_cards_B = f'{team_b} got {cards}  Yellow Cards in {len(dff_b[dff_b["y_cards_1"] >= cards]) / len(dff_b["y_cards_1"]) * 100:.2f}% of the last {pop_b} matches;\'' \
                     f'{team_b} got {cards}  Red Cards in {len(dff_b[dff_b["r_cards_1"] >= cards]) / len(dff_b["r_cards_1"]) * 100:.2f}% of the last {pop_b} matches;\'' \

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
           resume_goals_B, resume_corners_B, resume_cards_A, resume_cards_B

#EXECUTE
if __name__ == '__main__':
    app.run_server(debug=True)