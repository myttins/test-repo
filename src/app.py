import os

from flask import Flask, g, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

from src.db import db, Team, check_tables_exist
from src.model import train_model, predict_game
from src.nba_data import update_teams, update_players
from nba_api.live.nba.endpoints import scoreboard

load_dotenv()
app = Flask(__name__, static_folder=os.getcwd()+'/src/frontend/build', static_url_path='')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# migrate = Migrate(app, db)


with app.app_context():
    if not check_tables_exist(db.engine, ['team']):
        db.drop_all()
        db.create_all()


@app.before_request
def before_request_func():
    if not hasattr(g, 'updated_data'):
        update_teams()
        update_players()
        # update_games()
        g.updated_data = True


@app.route('/api/healthcheck')
def healthcheck():
    return 'ok', 200


@app.route('/api/teams')
def teams():
    all_teams = Team.query.order_by(Team.full_name).all()
    teams_data = [{"id": team.id, "name": team.full_name, "abbreviation": team.abbreviation} for team in all_teams]

    return {"teams": teams_data}


@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    home_team = data.get('homeTeam')
    away_team = data.get('awayTeam')

    if not home_team or not away_team:
        return jsonify({"error": "Missing team codes"}), 400

    model = train_model()  # todo get stored model
    prediction = predict_game(model, home_team, away_team)
    winner_prediction = home_team if prediction else away_team

    return jsonify({"predictedWinner": winner_prediction})


@app.route('/api/today')
def today():
    model = train_model()  # todo get stored model
    games = scoreboard.ScoreBoard().get_dict()['scoreboard']['games']

    formatted_games = []
    for game in games:
        home_team = game['homeTeam']['teamTricode']
        away_team = game['awayTeam']['teamTricode']

        home_victory = predict_game(model, home_team, away_team)
        winner_prediction = home_team if home_victory else away_team

        game_data = {
            "gameTimeUTC": game['gameTimeUTC'],
            "homeTeam": {
                "name": game['homeTeam']['teamName'],
                "city": game['homeTeam']['teamCity'],
                "code": home_team
            },
            "awayTeam": {
                "name": game['awayTeam']['teamName'],
                "city": game['awayTeam']['teamCity'],
                "code": away_team
            },
            "predictedWinner": winner_prediction
        }
        formatted_games.append(game_data)

    return jsonify({"gamesToday": formatted_games})


# these routes serve as a proxy for react frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    base_dir = os.getcwd() + '/src'

    if path != "" and os.path.exists(base_dir + "/frontend/build/" + path):
        return send_from_directory(base_dir + '/frontend/build', path)
    else:
        return send_from_directory(base_dir + '/frontend/build', 'index.html')


if __name__ == '__main__':
    app.run()
