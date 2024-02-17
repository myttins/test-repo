import os
from datetime import datetime

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import leaguegamefinder

from src.db import db, Team, Player, Game

proxy_url = os.environ.get('QUOTAGUARDSTATIC_URL') or None
team_game_headers = ['season',
                     'TEAM_ID',
                     'TEAM_ABBREVIATION',
                     'TEAM_NAME',
                     'game_id',
                     'GAME_DATE',
                     'MATCHUP',
                     'WIN_LOSS',
                     'MIN',
                     'PTS',
                     'FGM',
                     'FGA',
                     'FG_PCT',
                     'FG3M',
                     'FG3A',
                     'FG3_PCT',
                     'FTM',
                     'FTA',
                     'FT_PCT',
                     'offensive_reb',
                     'defensive_reb',
                     'rebounds',
                     'assists',
                     'steals',
                     'blocks',
                     'turnover',
                     'personal_foul',
                     'PLUS_MINUS']


def update_teams():
    for team_data in teams.get_teams():
        existing_team = db.session.get(Team, team_data['id'])
        if not existing_team:
            team = Team(id=team_data['id'],
                        full_name=team_data['full_name'],
                        abbreviation=team_data['abbreviation'],
                        nickname=team_data['nickname'])
            db.session.add(team)
    db.session.commit()


def update_players():
    active_players = [player for player in players.get_players() if player['is_active'] is True]
    for player_data in active_players:
        existing_player = db.session.get(Player, player_data['id'])
        if not existing_player:
            player = Player(id=player_data['id'],
                            full_name=player_data['full_name'],
                            first_name=player_data['first_name'],
                            last_name=player_data['last_name'])
            db.session.add(player)
    db.session.commit()


def update_games():
    season_games = get_all_season_games("2023-24")
    for game in season_games:
        game_id = game[4]
        existing_game = db.session.get(Game, game_id)
        if not existing_game:
            # extract basic data
            game_date = datetime.strptime(game[5], "%Y-%m-%d").date()
            matchup = game[6]
            teams = matchup.split(' vs. ') if ' vs. ' in matchup else matchup.split(' @ ')
            team_abbreviation = game[2]
            opponent = teams[1] if teams[0] == team_abbreviation else teams[0]
            won_game = True if game[7] == 'W' else False

            # extract stats
            points = game[9]
            rebounds = game[21]
            assists = game[22]

            # only add games with nba teams (there's some random international/exhibition games in this data)
            existing_team1 = Team.query.filter_by(abbreviation=team_abbreviation).first()
            existing_team2 = Team.query.filter_by(abbreviation=opponent).first()
            if existing_team1 is None or existing_team2 is None:
                continue

            # save to db
            new_game = Game(id=game_id, date=game_date, team=team_abbreviation,
                        opponent=opponent, won_game=won_game,
                        points=points, rebounds=rebounds, assists=assists)
            db.session.add(new_game)
    db.session.commit()


def get_all_season_games(season):
    return leaguegamefinder.LeagueGameFinder(season_nullable=season, league_id_nullable='00', proxy=proxy_url).get_dict()['resultSets'][0]['rowSet']
