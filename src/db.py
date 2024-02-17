from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.reflection import Inspector

db = SQLAlchemy()


def check_tables_exist(engine, table_names):
    inspector = Inspector.from_engine(engine)
    existing_tables = inspector.get_table_names()
    return all(table_name in existing_tables for table_name in table_names)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128), nullable=False)
    abbreviation = db.Column(db.String(3), nullable=False)
    nickname = db.Column(db.String(64), nullable=False)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    team = db.Column(db.String(3), nullable=False)
    opponent = db.Column(db.String(3), nullable=False)
    won_game = db.Column(db.Boolean, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    rebounds = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
