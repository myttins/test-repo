# NBA Matchup Predictor

### Prerequisites

- Python 3.9+
- pip

### Installing

1. Clone the repo.

2. Create a virtual env (optional)
    ```sh
    python3 -m venv venv && source venv/bin/activate
    ````

2. Install the backend/frontend requirements:
    ```sh
    pip install -r requirements.txt
    npm install --prefix src/frontend
    ````

3. Setup the flask app:
    ```sh
    export FLASK_APP=src/app.py
    ```

4. Build frontend:
    ```sh
    npm run build --prefix src/frontend
    ```

### Running Locally

1. Run tests:
    ```sh
    DATABASE_URL="sqlite:///:memory:" pytest
    ```

2. Run the flask app:
    ```sh
    flask run
    ```

## Built With

- [Flask](http://flask.pocoo.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [NBA Python API](https://pypi.org/project/nba_api/)