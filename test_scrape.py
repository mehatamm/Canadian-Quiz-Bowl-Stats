import requests
from bs4 import BeautifulSoup
import re
domain = "https://hsquizbowl.org/db/"
url = "https://hsquizbowl.org/db/tournaments/9209/stats/round_robin_%281-11%29/rounds/"



def get_games_from_round(round_url):
    response = requests.get(round_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        games = soup.find_all('table')[3:]
    game_csvs=[]
    for table in games:
        rows = table.find_all('tr')
        row_0_cols = rows[0].find_all('b')
        team_a = row_0_cols[0].get_text(strip=True)
        team_b = row_0_cols[6].get_text(strip=True)
        team_a_players = []
        team_b_players = []
        scoreline = table.find_previous_sibling().get_text(strip=True)
        if(scoreline[:len(team_a)]==team_a):
            score_a, score_b = scoreline[len(team_a)+1:].split(',', 1)
            score_b = score_b[len(team_b)+2:]
        else:
            score_b, score_a = scoreline[len(team_b)+1:].split(',', 1)
            score_a = score_b[len(team_a)+2:]
        
        for i in range(1, 5):
                fields = rows[i].find_all('td')
                player = fields[0].get_text(strip=True)
                if(player != "Total"):
                    team_a_players.append([player, fields[1].get_text(strip=True), fields[2].get_text(strip=True), fields[3].get_text(strip=True), fields[4].get_text(strip=True)])
                else:
                        break
        for i in range(1, 5):
                fields = rows[i].find_all('td')
                player = fields[7].get_text(strip=True)
                if(player != "Total"):
                    team_b_players.append([player, fields[8].get_text(strip=True), fields[9].get_text(strip=True), fields[10].get_text(strip=True), fields[11].get_text(strip=True)])
                else:
                        break
        game_csvs.append([team_a, team_b, score_a, score_b, team_a_players, team_b_players])
    return(game_csvs)    

playtime_url = "https://hsquizbowl.org/db/tournaments/9116/stats/combined/games/#round-3"
games = get_games_from_round(playtime_url)