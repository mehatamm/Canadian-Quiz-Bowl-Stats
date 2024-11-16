import requests
from bs4 import BeautifulSoup
import numpy as np

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
               ["SCT D1 2023", "https://hsquizbowl.org/db/tournaments/7863/stats/d1_finals/games/", "sqbs"],
               ]

#structure of game:
#[[team_name_a, [player_1, ...]], team_a_pts, [team_name_b, [player_2, ...]], team_b_pts]
#structure of player:
#[player_name, tuh, powers, tens, negs]

def tu_points(team):
    s = 0
    for player in team:
        s+= 15*player[2]+10*player[3]-5*player[4]
    return s
def parse_team_line_sqbs(team_line, tu_per_game):
    team_name, players = team_line.split(': ')
    players = players.split(', ')
    team_players = []
    for player in players:
        name = player[:player.find('(')-1]
        player = player[player.find(')')+2:]
        scores = [int(word) for word in player.split()[:3]]
        team_players.append([name, 24]+scores)
    return team_name, team_players
def get_games_from_rounds_sqbs(scoreboard_url, tu_per_game):
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
        a_name, a_players = parse_team_line_sqbs(stripped_lines[0], tu_per_game)
        b_name, b_players = parse_team_line_sqbs(stripped_lines[1], tu_per_game)
        bpts_a, bpts_b = [int(word) for word in stripped_lines[2].split() if word.isdigit()][1::2]
        
        game_reports.append([a_name, b_name, bpts_a+tu_points(a_players), bpts_b+tu_points(b_players), a_players, b_players])
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
                    team_a_players.append([player, int(fields[1].get_text(strip=True)), int(fields[2].get_text(strip=True)), int(fields[3].get_text(strip=True)), int(fields[4].get_text(strip=True))])
                else:
                        break
        for i in range(1, 5):
                fields = rows[i].find_all('td')
                player = fields[7].get_text(strip=True)
                if(player != "Total"):
                    team_b_players.append([player, int(fields[8].get_text(strip=True)), int(fields[9].get_text(strip=True)), int(fields[10].get_text(strip=True)), int(fields[11].get_text(strip=True))])
                else:
                        break
        game_csvs.append([team_a, team_b, score_a, score_b, team_a_players, team_b_players])
    return(game_csvs)    

dtype = [("tournament_name", "U100"), ("team_a", "U100"), ("team_a_score", "i4"), 
         ("team_a_player_1", "U50"), ("team_a_player_1_tuh", "i4"), ("team_a_player_1_powers", "i4"), ("team_a_player_1_gets", "i4"), ("team_a_player_1_negs", "i4"),
         ("team_a_player_2", "U50"), ("team_a_player_2_tuh", "i4"), ("team_a_player_2_powers", "i4"), ("team_a_player_2_gets", "i4"), ("team_a_player_2_negs", "i4"),
         ("team_a_player_3", "U50"), ("team_a_player_3_tuh", "i4"), ("team_a_player_3_powers", "i4"), ("team_a_player_3_gets", "i4"), ("team_a_player_3_negs", "i4"),
         ("team_a_player_4", "U50"), ("team_a_player_4_tuh", "i4"), ("team_a_player_4_powers", "i4"), ("team_a_player_4_gets", "i4"), ("team_a_player_4_negs", "i4"),
         ("team_b", "U100"), ("team_b_score", "i4"), 
         ("team_b_player_1", "U50"), ("team_b_player_1_tuh", "i4"), ("team_b_player_1_powers", "i4"), ("team_b_player_1_gets", "i4"), ("team_b_player_1_negs", "i4"),
         ("team_b_player_2", "U50"), ("team_b_player_2_tuh", "i4"), ("team_b_player_2_powers", "i4"), ("team_b_player_2_gets", "i4"), ("team_b_player_2_negs", "i4"),
         ("team_b_player_3", "U50"), ("team_b_player_3_tuh", "i4"), ("team_b_player_3_powers", "i4"), ("team_b_player_3_gets", "i4"), ("team_b_player_3_negs", "i4"),
         ("team_b_player_4", "U50"), ("team_b_player_4_tuh", "i4"), ("team_b_player_4_powers", "i4"), ("team_b_player_4_gets", "i4"), ("team_b_player_4_negs", "i4"),
         ]

def urls_to_nparray(url_list):
    games_list = []
    for elem in url_list:
        if(len(elem) == 3):
            tname, url, _ = elem
            games = get_games_from_rounds_sqbs(url, 24)
        else:
            name, url = elem
            games = get_games_from_rounds(url)
        for game in games:
            team_a, team_b, score_a, score_b, players_a, players_b = game
            for _ in range(4-len(players_a)):
                players_a.append(["None", 0, 0, 0, 0])
            for _ in range(4-len(players_b)):
                players_b.append(["None", 0, 0, 0, 0])
            games_list.append((tname, team_a, score_a, 
            players_a[0][0], players_a[0][1], players_a[0][2], players_a[0][3], players_a[0][4],
            players_a[1][0], players_a[1][1], players_a[1][2], players_a[1][3], players_a[1][4],
            players_a[2][0], players_a[2][1], players_a[2][2], players_a[2][3], players_a[2][4],
            players_a[3][0], players_a[3][1], players_a[3][2], players_a[3][3], players_a[3][4],
            team_b, score_b,
            players_b[0][0], players_b[0][1], players_b[0][2], players_b[0][3], players_b[0][4],
            players_b[1][0], players_b[1][1], players_b[1][2], players_b[1][3], players_b[1][4],
            players_b[2][0], players_b[2][1], players_b[2][2], players_b[2][3], players_b[2][4],
            players_b[3][0], players_b[3][1], players_b[3][2], players_b[3][3], players_b[3][4],)
            )
    games = np.array(games_list, dtype=dtype)
    return games
#playtime_url = "https://hsquizbowl.org/db/tournaments/9116/stats/combined/games/#round-3"
#games = get_games_from_rounds(playtime_url)
#print(games[0])
#games = get_games_from_rounds_sqbs(sct_url)

urls = [["SCT D1 2023", "https://hsquizbowl.org/db/tournaments/7863/stats/d1_finals/games/", "sqbs"]]
df = urls_to_nparray(urls)
print(df)