from datetime import date

from src.db import Player, Team, Game


def test_new_team(db, app):
    with app.app_context():
        team = Team(full_name="Denver Nuggets", abbreviation="DEN", nickname="Nuggets")
        db.session.add(team)
        db.session.commit()
        assert team.full_name == "Denver Nuggets"
        assert team.abbreviation == "DEN"
        assert team.nickname == "Nuggets"


def test_new_player(db, app):
    with app.app_context():
        player = Player(full_name="Jamal Murray", first_name="Jamal", last_name="Murray")
        db.session.add(player)
        db.session.commit()
        assert player.full_name == "Jamal Murray"
        assert player.first_name == "Jamal"
        assert player.last_name == "Murray"


def test_new_game(db, app):
    with app.app_context():
        new_game = Game(id=12345, date=date(2023, 10, 1), team="DEN", opponent="CLP", won_game=True, points=110, rebounds=44, assists=26)
        db.session.add(new_game)
        db.session.commit()

        added_game = Game.query.get(12345)

        assert added_game is not None
        assert added_game.date == date(2023, 10, 1)
        assert added_game.team == "DEN"
        assert added_game.opponent == "CLP"
        assert added_game.won_game is True
        assert added_game.points == 110
        assert added_game.rebounds == 44
        assert added_game.assists == 26
