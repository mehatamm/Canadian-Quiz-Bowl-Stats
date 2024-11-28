import pandas as pd

neg_columns = ["team_a_player_1_negs", "team_a_player_2_negs", "team_a_player_3_negs", "team_a_player_4_negs", 
               "team_b_player_1_negs", "team_b_player_2_negs", "team_b_player_3_negs", "team_b_player_4_negs"]

power_columns = ["team_a_player_1_powers", "team_a_player_2_powers", "team_a_player_3_powers", "team_a_player_4_powers", 
               "team_b_player_1_powers", "team_b_player_2_powers", "team_b_player_3_powers", "team_b_player_4_powers"]

player_a_cols = ["team_a_player_1", "team_a_player_2", "team_a_player_3", "team_a_player_4"]

player_b_cols = ["team_b_player_1", "team_b_player_2", "team_b_player_3", "team_b_player_4"]

df = pd.read_csv("games.csv")

max_row = (df[neg_columns].max(axis=1)).idxmax()

df['max_negs'] = df[neg_columns].max(axis=1)
sorted_df = df.sort_values(by='max_negs', ascending=False)

n = 100

top_indices = sorted_df.head(n).index.tolist()

x=2

xneg_indices = df[df["max_negs"] >= x].index.tolist()

min_negs = df.loc[top_indices[-1]]["max_negs"]

#for index in top_indices:
#    print(df.loc[index])

def extract_players(indices):
    players = []
    for index in indices:
        row = df.loc[index]
        for col in neg_columns:
            if row[col]==row["max_negs"]:
                name = row[col[:-5]]
                players.append(name)
    freq_list = pd.Series(players).value_counts()
    print(freq_list)

def extract_players_negs_ge(indices, x):
    players = []
    for index in indices:
        row = df.loc[index]
        for col in neg_columns:
            if row[col]>=x:
                name = row[col[:-5]]
                players.append(name)
    freq_list = pd.Series(players).value_counts()
    print(freq_list.head(20))

def get_total_negs():
    players = []
    for index, row in df.iterrows():
        for col in neg_columns:
            name = row[col[:-5]]
            if row[col] !=0:
                for i in range(row[col]):
                    players.append(name)
    freq_list = pd.Series(players).value_counts()
    print(freq_list.head(20))

def get_frequent_matchups():
    mus = dict()
    for index, row in df.iterrows():
        for a_col in player_a_cols:
            for b_col in player_b_cols:
                if(isinstance(row[a_col], str) and isinstance(row[b_col], str)):
                    score = [1, 0] if row["team_a_score"]>row["team_b_score"] else [0, 1]
                    if(row[a_col]>row[b_col]):
                        if (row[a_col], row[b_col]) in mus:
                            mus[(row[a_col], row[b_col])][0] += score[0]
                            mus[(row[a_col], row[b_col])][1] += score[1]
                        else:
                            mus[(row[a_col], row[b_col])] = score
                    else:
                        if (row[b_col], row[a_col]) in mus:
                            mus[(row[b_col], row[a_col])][0] += score[1]
                            mus[(row[b_col], row[a_col])][1] += score[0]
                        else:
                            mus[(row[b_col], row[a_col])] = [score[1], score[0]]
    mus_sorted = sorted(mus.items(), key=lambda item: item[1][0]+item[1][1], reverse=True)[:100]

    for key, value in mus_sorted:
        print(f"{key[0]} - {key[1]}: {value[0]} - {value[1]}")


#print(f"Players by frequency in the top {n} highest canadian circuit single-game neg performances since the start of the 2022 season (minimum negs: {min_negs}):")
#extract_players(top_indices)

#print(f"Players by games with at least {x} negs")
#extract_players_negs_ge(xneg_indices, x)

#print("Players by total negs in canadian circuit games since the start of the 2022 season")
#get_total_negs()

print("Most common matchups:")
get_frequent_matchups()