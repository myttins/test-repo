from datetime import datetime

import pandas as pd

from src.nba_data import get_all_season_games


def update_games_to_csv():
    season_games = get_all_season_games("2023-24")
    games_list = []
    for game in season_games:
        game_id = game[4]
        game_date = datetime.strptime(game[5], "%Y-%m-%d").date()
        matchup = game[6]
        teams_split = matchup.split(' vs. ') if ' vs. ' in matchup else matchup.split(' @ ')
        team_abbreviation = game[2]
        opponent = teams_split[1] if teams_split[0] == team_abbreviation else teams_split[0]
        won_game = True if game[7] == 'W' else False

        points = game[9]
        rebounds = game[21]
        assists = game[22]

        game_data = {
            "game_id": game_id, "game_date": game_date, "team_abbreviation": team_abbreviation,
            "opponent": opponent, "won_game": won_game, "points": points,
            "rebounds": rebounds, "assists": assists
        }
        games_list.append(game_data)

    games_df = pd.DataFrame(games_list)
    games_df.to_csv('data/nba_games.csv', index=False)


if __name__ == "__main__":
    update_games_to_csv()