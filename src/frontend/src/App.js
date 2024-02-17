import React, { useEffect, useState } from "react";
import './App.css';

function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [games, setGames] = useState([]);
    const [teams, setTeams] = useState([]);
    const [predictedWinner, setPredictedWinner] = useState('');
    const [homeTeam, setHomeTeam] = useState('');
    const [awayTeam, setAwayTeam] = useState('');

    const pickRandomTeams = (teams) => {
        let homeIndex = Math.floor(Math.random() * teams.length);
        let awayIndex;
        do {
            awayIndex = Math.floor(Math.random() * teams.length);
        } while (homeIndex === awayIndex); // don't want to pick the same team for home/away

        setHomeTeam(teams[homeIndex].abbreviation);
        setAwayTeam(teams[awayIndex].abbreviation);
    };

    useEffect(() => {
        setIsLoading(true);
        Promise.all([
            fetch('/api/today')
                .then(response => response.json())
                .then(data => setGames(data.gamesToday)),
            fetch('/api/teams')
                .then(response => response.json())
                .then(data => {
                    setTeams(data.teams);
                    pickRandomTeams(data.teams);
                })
        ]).then(() => {
            setIsLoading(false);
        }).catch(error => {
            console.error("Failed to fetch data:", error);
        });
    }, []);

    if (isLoading) {
        return <div className="loading">Loading...</div>;
    }

    const renderGames = () => {
        return games.map((game, index) => (
            <div key={index} className="gameContainer">
                <div className="gameTime">{new Date(game.gameTimeUTC).toLocaleTimeString()}</div>
                <div className="gameDetails">
                    <p>{game.awayTeam.city} {game.awayTeam.name} @ {game.homeTeam.city} {game.homeTeam.name}</p>
                    <p>Predicted Winner: {game.predictedWinner}</p>
                </div>
            </div>
        ));
    };

    const handlePrediction = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const homeTeam = formData.get('homeTeam');
        const awayTeam = formData.get('awayTeam');

        fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ homeTeam, awayTeam })
        })
            .then(response => response.json())
            .then(data => {
                setPredictedWinner(`Predicted Winner: ${data.predictedWinner}`);
            })
            .catch(error => console.error("Failed to predict the game:", error));
    };

    return (
        <div className="App">
            <header className="header">
                <h1>Predictions for Today's NBA Games</h1>
            </header>

            <div className="gamesList">{renderGames()}</div>

            <hr></hr>

            <div className="predictionComponent">
                <h2>Predict a Game</h2>

                {predictedWinner && <p className="predictionResult">{predictedWinner}</p>}

                <form onSubmit={handlePrediction} className="predictionForm">
                    <div>
                        <label htmlFor="homeTeam">Home Team:</label>
                        <select id="homeTeam" name="homeTeam" required defaultValue={homeTeam}>
                            {teams.map(team => (
                                <option key={team.abbreviation} value={team.abbreviation}>{team.name}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                    <label htmlFor="awayTeam">Away Team:</label>
                        <select id="awayTeam" name="awayTeam" required defaultValue={awayTeam}>
                            {teams.map(team => (
                                <option key={team.abbreviation} value={team.abbreviation}>{team.name}</option>
                            ))}
                        </select>
                    </div>

                    <button type="submit">Predict Winner</button>
                </form>
            </div>
        </div>
    );
}

export default App;