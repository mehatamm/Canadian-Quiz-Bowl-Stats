import pandas as pd

neg_columns = ["team_a_player_1_negs", "team_a_player_2_negs", "team_a_player_3_negs", "team_a_player_4_negs", 
               "team_b_player_1_negs", "team_b_player_2_negs", "team_b_player_3_negs", "team_b_player_4_negs"]

power_columns = ["team_a_player_1_powers", "team_a_player_2_powers", "team_a_player_3_powers", "team_a_player_4_powers", 
               "team_b_player_1_powers", "team_b_player_2_powers", "team_b_player_3_powers", "team_b_player_4_powers"]

df = pd.read_csv("games.csv")

max_row = (df[neg_columns].max(axis=1)).idxmax()

df['max_negs'] = df[neg_columns].max(axis=1)
sorted_df = df.sort_values(by='max_negs', ascending=False)

n = 100

top_indices = sorted_df.head(n).index.tolist()

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
                if "(UG)" in name:
                    name = name[:-5]
                if "(DII)" in name:
                    name = name[:-6]
                players.append(name)
    freq_list = pd.Series(players).value_counts()
    print(freq_list)

print(f"Players by frequency in the top {n} highest canadian circuit single-game neg performances since the start of the 2022 season (minimum negs: {min_negs}):")
extract_players(top_indices)
#print(result_row)