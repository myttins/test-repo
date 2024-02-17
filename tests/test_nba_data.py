from unittest.mock import patch

from src.db import Player, Team
from src.nba_data import update_teams, update_players


mock_teams_response = [
    {
        'id': 1,
        'full_name': 'Mock Team 1',
        'abbreviation': 'MT1',
        'nickname': 'Mockers1'
    },
    {
        'id': 2,
        'full_name': 'Mock Team 2',
        'abbreviation': 'MT2',
        'nickname': 'Mockers2'
    },
]

mock_players_response = [
    {
        'id': 101,
        'full_name': 'Mock Player 1',
        'first_name': 'Mock1',
        'last_name': 'Player1',
        'is_active': True
    },
    {
        'id': 102,
        'full_name': 'Mock Player 2',
        'first_name': 'Mock2',
        'last_name': 'Player2',
        'is_active': True
    },
]


@patch('nba_api.stats.static.teams.get_teams', return_value=mock_teams_response)
def test_update_teams(mock_get_teams, db, app):
    with app.app_context():
        assert Team.query.count() == 0
        update_teams()
        assert Team.query.count() == 2


@patch('nba_api.stats.static.players.get_players', return_value=mock_players_response)
def test_update_players(mock_get_players, db, app):
    with app.app_context():
        assert Player.query.count() == 0
        update_players()
        assert Player.query.count() == 2
