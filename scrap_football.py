import bs4
import requests
import time
import pandas as pd
import numpy as np

laLiga = {'name': 'LaLiga', 'link': 'https://fbref.com/pt/comps/12/cronograma/La-Liga-Resultados-e-Calendarios', 'match_sched': 'div_sched_2022-2023_12_1'}
premier = {'name': 'Premier', 'link': 'https://fbref.com/pt/comps/9/cronograma/Premier-League-Resultados-e-Calendarios','match_sched': 'sched_2022-2023_9_1'}
italy = {'name': 'Italy-A', 'link': 'https://fbref.com/pt/comps/11/cronograma/Serie-A-Resultados-e-Calendarios', 'match_sched': 'div_sched_2022-2023_11_1'}
france = {'name': 'France-1', 'link': 'https://fbref.com/pt/comps/13/cronograma/Ligue-1-Resultados-e-Calendarios', 'match_sched': 'div_sched_2022-2023_13_1'}
bundesliga = {'name': 'Bundesliga', 'link': 'https://fbref.com/pt/comps/20/cronograma/Bundesliga-Resultados-e-Calendarios', 'match_sched': 'div_sched_2022-2023_20_1'}
portugal = {'name':'PrimeiraLiga','link':'https://fbref.com/pt/comps/32/cronograma/Primeira-Liga-Resultados-e-Calendarios', 'match_sched': 'div_sched_2022-2023_32_1'}
competitions = [premier, italy, france, bundesliga, portugal]


def get_schedule(url, id_table):
    # Link da tabela de jogos:
    url = url
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text,
                             "html.parser")
    # componente contendo a tabela de jogos com os links
    tabela_jogos = soup.find(id=id_table)
    # procura por todos os elementos <a> dentro da tabela
    href_links = tabela_jogos.find_all("a")
    # cria uma lista para conter os links dentro da tabela
    lista_links = []
    # adiciona à lista apenas os links, fora da tag
    for aux in href_links:
        lista_links.append(aux['href'])
    # cria uma lista para conter apenas os links relacionados à partidas
    links_partidas = []
    # adiciiona à lista apenas os links relacionados a par
    for links in lista_links:
        aux = links.split("/")
        if aux[2] == "partidas" and len(aux) > 4:
            links_partidas.append(aux)
    final_links = []
    [final_links.append(x) for x in links_partidas if x not in final_links]
    request_links = []

    for aux in final_links:
        request_links.append('https://fbref.com/pt/partidas/' + aux[3] + "/" + aux[4])

    request_links

    return request_links

def get_match_stats(link, league):
    url = link
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")

    content = soup.find(id='content')
    # header of match (confront + date)
    header = content.find('h1')
    confronto = header.text.split('–')[0].replace('Relatório da Partida', '')
    team_1 = confronto.split('vs')[0].replace(' ', '')
    team_2 = confronto.split('vs')[1].replace(' ', '').replace('.', '')

    date = header.text.split('–')[1]

    score_1 = int(content.find_all('div', {'class': 'score'})[0].text)
    score_2 = int(content.find_all('div', {'class': 'score'})[1].text)

    strongs = content.find_all('strong')

    all_stats = []

    for st in strongs[-8::]:
        stat = st.text.replace('%', '')
        if (stat != ""):
            all_stats.append(float(stat) / 100)
        else:
            all_stats.append(0)

    posse_1 = all_stats[0]
    posse_2 = all_stats[1]
    acerto_1 = all_stats[2]
    acerto_2 = all_stats[3]
    chutes_1 = all_stats[4]
    chutes_2 = all_stats[5]
    defesas_1 = all_stats[6]
    defesas_2 = all_stats[7]

    cards_total = content.find_all('div', {'class': 'cards'})
    y_cards_1 = len(cards_total[0].find_all('span', {'class': 'yellow_card'}))
    y_cards_2 = len(cards_total[1].find_all('span', {'class': 'yellow_card'}))
    r_cards_1 = len(cards_total[0].find_all('span', {'class': 'red_card'}))
    r_cards_2 = len(cards_total[1].find_all('span', {'class': 'red_card'}))

    extra_stats = content.find('div', id='team_stats_extra').find_all('div')

    faltas_1 = int(f'0{extra_stats[4].text}')
    faltas_2 = int(f'0{extra_stats[6].text}')
    escanteios_1 = int(f'0{extra_stats[7].text}')
    escanteios_2 = int(f'0{extra_stats[9].text}')
    cruzamentos_1 = int(f'0{extra_stats[10].text}')
    cruzamentos_2 = int(f'0{extra_stats[12].text}')
    contatos_1 = int(f'0{extra_stats[13].text}')
    contatos_2 = int(f'0{extra_stats[15].text}')
    jogada_aerea_1 = int(f'0{extra_stats[26].text}')
    jogada_aerea_2 = int(f'0{extra_stats[28].text}')
    defesas_1 = int(f'0{extra_stats[29].text}')
    defesas_2 = int(f'0{extra_stats[31].text}')
    impedimento_1 = int(f'0{extra_stats[36].text}')
    impedimento_2 = int(f'0{extra_stats[38].text}')
    tiro_meta_1 = int(f'0{extra_stats[39].text}')
    tiro_meta_2 = int(f'0{extra_stats[41].text}')
    lateral_1 = int(f'0{extra_stats[42].text}')
    lateral_2 = int(f'0{extra_stats[44].text}')

    return [team_1, team_2, date, score_1, score_2, posse_1, posse_2, acerto_1, acerto_2, chutes_1, chutes_2, defesas_1,
            defesas_2, y_cards_1, y_cards_2, r_cards_1, r_cards_2, faltas_1, faltas_2, \
            escanteios_1, escanteios_2, cruzamentos_1, cruzamentos_2, contatos_1, contatos_2, jogada_aerea_1,
            jogada_aerea_2, defesas_1, defesas_2, impedimento_1, impedimento_2, tiro_meta_1, tiro_meta_2, \
            lateral_1, lateral_2, 'home', league], \
           [team_2, team_1, date, score_2, score_1, posse_2, posse_1, acerto_2, acerto_1, chutes_2, chutes_1, defesas_2,
            defesas_1, y_cards_2, y_cards_1, r_cards_2, r_cards_1, faltas_2, faltas_1, \
            escanteios_2, escanteios_1, cruzamentos_2, cruzamentos_1, contatos_2, contatos_1, jogada_aerea_2,
            jogada_aerea_1, defesas_2, defesas_1, impedimento_2, impedimento_1, tiro_meta_2, tiro_meta_1, \
            lateral_2, lateral_1, 'away', league]

def update_csvFile(competitions, old_df):
    match_stats = []
    # The df has to have the same "league" name for checking
    for comp in competitions:
        # filter the DataFrame according to the league
        dff = old_df[old_df['league'] == comp['name']]
        # Counts how many matches have been played untill now
        matches_count = len(get_schedule(comp['link'], comp['match_sched']))
        # If there is more matches played than what have been scraped already
        print(f'{comp["name"]} ---- Matches played: {matches_count} \nMatchesDownoloaded: {len(dff) / 2}')
        if (matches_count > len(dff) / 2):
            # Download what is missing
            sched = get_schedule(comp['link'], comp['match_sched'])
            for i in range(int(len(dff) / 2), matches_count):
                print(sched[i])
                a, b = get_match_stats(sched[i], comp['name'])
                print(a)
                print(b)
                match_stats.append(a)
                match_stats.append(b)
                time.sleep(3)
    header = ['team_1', 'team_2', 'date', 'score_1', 'score_2', 'posse_1', 'posse_2', 'acerto_1', 'acerto_2',
              'chutes_1', \
              'chutes_2', 'defesas_1', 'defesas_2', 'y_cards_1', 'y_cards_2', 'r_cards_1', 'r_cards_2', 'faltas_1',
              'faltas_2', \
              'escanteios_1', 'escanteios_2', 'cruzamentos_1', 'cruzamentos_2', 'contatos_1', 'contatos_2',
              'jogada_aerea_1', \
              'jogada_aerea_2', 'defesas_1', 'defesas_2', 'impedimento_1', 'impedimento_2', 'tiro_meta_1',
              'tiro_meta_2', \
              'lateral_1', 'lateral_2', 'home_away', 'league']
    new_df = pd.DataFrame(data=match_stats, columns=header)

    return new_df

def update_csv_matches():
    old_df = pd.read_csv('data.csv')

    new_df = update_csvFile(competitions, old_df)
    print(new_df.head(5))
    print(old_df.head(5))
    new_df.to_csv('data.csv', index=False, header=False, mode='a')

