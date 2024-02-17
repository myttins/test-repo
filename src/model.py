import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.db import Game

team_to_int_dict = {'TT': 99, 'FF': 100}


# def get_season_df() -> pd.DataFrame:
#     games = Game.query.all()
#
#     # convert into a dataframe
#     games_list = [{"date": game.date, "team": game.team, "opponent": game.opponent,
#                    "won_game": game.won_game, "points": game.points,
#                    "rebounds": game.rebounds, "assists": game.assists}
#                   for game in games]
#     games_df = pd.DataFrame(games_list)
#
#     return games_df

def get_season_df():
    games_df = pd.read_csv('data/nba_games.csv')
    return games_df


def train_model():
    games_df = get_season_df()

    # reverse and concatenate the season data, so we have data points from both perspectives
    games_df_reversed = games_df.rename(columns={"team": "opponent", "opponent": "team", "won_game": "lost_game"})
    games_df_reversed["lost_game"] = games_df_reversed["lost_game"].apply(lambda x: not x)
    training_data = pd.concat([games_df, games_df_reversed.rename(columns={"lost_game": "won_game"})], ignore_index=True)

    # map team ids to ints for encoding
    teams = pd.unique(training_data[['team', 'opponent']].values.ravel('K'))
    for i, team in enumerate(teams):
        team_to_int_dict[team] = i

    # encode features/target
    training_data['won_game_encoded'] = training_data['won_game'].astype(int)
    training_data['team_encoded'] = training_data['team'].map(team_to_int_dict)
    training_data['opponent_encoded'] = training_data['opponent'].map(team_to_int_dict)

    # train the model
    X = training_data[['team_encoded', 'opponent_encoded']]
    y = training_data['won_game_encoded']
    model = LogisticRegression()
    model.fit(X.values, y.values)

    return model


# returns True if team1 is predicted to win, or False for team2
# predicts the home team to win in the case of ties
def predict_game(model, home_team: str, away_team: str) -> bool:
    home_team_id = team_to_int_dict[home_team]
    away_team_id = team_to_int_dict[away_team]

    X_new = np.array([[home_team_id, away_team_id]])
    prediction = model.predict_proba(X_new)
    home_win_probability = prediction[0][1]

    return home_win_probability >= 0.5
