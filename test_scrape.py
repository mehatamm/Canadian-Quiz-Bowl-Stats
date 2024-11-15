import requests
from bs4 import BeautifulSoup
import re
domain = "https://hsquizbowl.org/db/"
url = "https://hsquizbowl.org/db/tournaments/9209/stats/round_robin_%281-11%29/rounds/"

tournaments = [["Penn Bowl 2024", "https://hsquizbowl.org/db/tournaments/9209/stats/round_robin_%281-11%29/games/#round-1"],
               ["Penn Bowl 2024", "https://hsquizbowl.org/db/tournaments/9209/stats/finals/games/#round-12"],
               ["PLAYTIME!", "https://hsquizbowl.org/db/tournaments/9116/stats/combined/games/#round-1"],
               ["ACF Fall 2024", "https://hsquizbowl.org/db/tournaments/9045/stats/fixed_combined/games/#round-1"],
               ["NAQT Novice Toronto 2024", "https://hsquizbowl.org/db/tournaments/9057/stats/all_games_%28raw%29/games/#round-1"],
               ["NAQT Novice McGill 2024", "https://hsquizbowl.org/db/tournaments/9073/stats/all_games/games/#round-1"],
               ["CREEK", "https://hsquizbowl.org/db/tournaments/8843/stats/all_games/games/#round-1"],
               ["ESPN", "https://hsquizbowl.org/db/tournaments/8753/stats/prelims_%2B_playoffs/games/#round-1"],
               ["Booster Shot", "https://hsquizbowl.org/db/tournaments/8758/stats/combined%2Bfinals/games/#round-1"],
               ["SCT D2 2024", "https://hsquizbowl.org/db/tournaments/8703/stats/d2_all/games/#round-1"],
               ["SCT D1 2024", "https://hsquizbowl.org/db/tournaments/8703/stats/d1/games/#round-1"],
               ["ACF Regionals 2024", "https://hsquizbowl.org/db/tournaments/8698/stats/prelims/games/#round-1"],
               ["ACF Regionals 2024", "https://hsquizbowl.org/db/tournaments/8698/stats/finals/rounds/"],
               ["ILLIAC", "https://hsquizbowl.org/db/tournaments/8679/stats/all_games/games/#round-1"],
               ["ACF Winter 2023", "https://hsquizbowl.org/db/tournaments/8536/stats/combined/games/#round-1"],
               ["ACF Fall 2023", "https://hsquizbowl.org/db/tournaments/8328/stats/playoffs/games/#round-1"],
               ["Penn Bowl 2023", "https://hsquizbowl.org/db/tournaments/8397/stats/combined/games/#round-1"],
               ["DMA", "https://hsquizbowl.org/db/tournaments/8423/stats/combined/games/#round-1"],
               ["Arcadia 2023", "https://hsquizbowl.org/db/tournaments/8529/stats/all_games/games/#round-1"],
               ["C++", "https://hsquizbowl.org/db/tournaments/7944/stats/combined/games/#round-1"],
               ["ACF Regionals 2023", "https://hsquizbowl.org/db/tournaments/7982/stats/combined/games/#round-1"],
               ["SCT D2 2023", "https://hsquizbowl.org/db/tournaments/7863/stats/d2_all/games/#round-1"],
               ["SCT D1 2023", ]]

def parse_team_line(team_line):
    team_name, players = team_line.split(': ')
    players = players.split(', ')
    team = [team_name]
    for player in players:
        name = player[:player.find('(')-1]
        player = player[player.find(')')+2:]
        scores = [int(word) for word in player.split()[:3]]
        team.append([[name]+scores])
    return team
def get_games_from_rounds_sqbs(scoreboard_url):
    response = requests.get(scoreboard_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        raise ValueError("Website {scoreboard_url} not accessible")
    #print(soup.prettify())
    games = soup.find_all('font', {'size': '-1'})
    game_reports = []
    for game in games:
        stripped_lines = [line.strip() for line in game.stripped_strings]
        team_a = parse_team_line(stripped_lines[0])
        team_b = parse_team_line(stripped_lines[1])
        bpts_a, bpts_b = [int(word) for word in stripped_lines[2].split() if word.isdigit()][1::2]
        game_reports.append([team_a, bpts_a, team_b, bpts_b])
    return game_reports
def get_games_from_rounds(rounds_url):
    response = requests.get(rounds_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        games = soup.find_all('table')[3:]
    else:
        raise ValueError("Website {rounds_url} not accessible")
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

#playtime_url = "https://hsquizbowl.org/db/tournaments/9116/stats/combined/games/#round-3"
#games = get_games_from_rounds(playtime_url)

sct_url = "https://hsquizbowl.org/db/tournaments/7863/stats/d1_finals/games/"
games = get_games_from_rounds_sqbs(sct_url)
for game in games:
     print(game)