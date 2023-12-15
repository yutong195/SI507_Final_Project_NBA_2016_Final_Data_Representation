from flask import Flask, render_template, request, redirect, url_for
import json
import plotly
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

# Load your JSON data here
with open('nba_finals_tree.json', 'r') as file:
    data = json.load(file)

# Process the data into a format suitable for plotting
game_scores = []
for game in data['children']:
    game_number = game['name']
    game_data = {'game': game_number}
    for team in game['children']:
        team_name = team['name']
        # Finding the node with team totals
        team_totals = next((node for node in team['children'] if node['name'] == 'Team Totals'), None)
        if team_totals:
            game_data[team_name] = int(team_totals['data']['PTS'])
    game_scores.append(game_data)

# Preparing data for the bar plot
teams = list(set(team for score in game_scores for team in score if team != 'game'))
team_scores = {team: [] for team in teams}
games = []

for score in game_scores:
    games.append(score['game'])
    for team in teams:
        team_scores[team].append(score.get(team, 0))

# Creating the bar plot using Plotly
fig = go.Figure()

for team in teams:
    fig.add_trace(go.Bar(name=team, x=games, y=team_scores[team]))

fig.update_layout(barmode='group', title='NBA Finals Scores by Game')

@app.route('/')
def index():
    # Convert the figures to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Calculate the player points data for the pie chart
    pie_data = calculate_player_points_data(data)

    # Create pie charts for each game and team
    pie_charts = create_pie_charts(pie_data)

    # Calculate the scores by quarter for the line chart
    line_chart_data = calculate_scores_by_quarter(data)

    # Render the index template with the graph
    return render_template('index.html', graphJSON=graphJSON, pie_charts=pie_charts, line_chart_data=line_chart_data)

def calculate_player_points_data(data):
    player_points_data = []

    for game in data['children']:
        game_name = game['name']
        for team in game['children']:
            team_name = team['name']
            for player in team['children']:
                if player['name'] != "Team Totals":
                    player_name = player['name']
                    player_points = player['data'].get('PTS', 0)
                    player_points_data.append({
                        'game': game_name,
                        'team': team_name,
                        'player': player_name,
                        'points': player_points
                    })

    return player_points_data

def create_pie_charts(pie_data):
    pie_charts = {}

    for game_data in pie_data:
        game_number = game_data['game']
        team_name = game_data['team']
        player_name = game_data['player']
        points = game_data['points']

        if game_number not in pie_charts:
            pie_charts[game_number] = {}

        if team_name not in pie_charts[game_number]:
            pie_charts[game_number][team_name] = []

        pie_charts[game_number][team_name].append({
            'player': player_name,
            'points': points
        })

    return pie_charts

def calculate_scores_by_quarter(data):
    scores_by_quarter = {}

    for game in data['children']:
        game_name = game['name']
        scores_by_quarter[game_name] = {'Cavaliers': [], 'Warriors': []}
        
        for team in game['children']:
            team_name = team['name']
            if team_name not in ['Cavaliers', 'Warriors']:
                continue
            
            # Initialize the scores list for this team and game
            team_scores = []
            for quarter_info in team['children']:
                if quarter_info['name'] == 'Quarter Data':
                    # Assuming the quarters are labeled as '1st', '2nd', '3rd', '4th', and 'OT' if exists
                    for quarter in ['1st', '2nd', '3rd', '4th']:
                        if quarter in quarter_info['data']:
                            team_scores.append(quarter_info['data'][quarter]['FG%'])
                        else:
                            
                            team_scores.append(0)
            
            # Assign the scores list to the corresponding team and game
            scores_by_quarter[game_name][team_name] = team_scores

    return scores_by_quarter


#This is for data comparison between key players
@app.route('/select_game_for_player')
def select_game_for_player():
    # Extracting game names
    games = [game['name'] for game in data['children']]
    return render_template('select_game_for_player.html', games=games)

@app.route('/select_players/<game_name>')
def select_players(game_name):
    # Finding the selected game data
    selected_game = next((game for game in data['children'] if game['name'] == game_name), None)
    if not selected_game:
        return "Game not found", 404

    # Extracting team names and their players
    team_players = {}
    for team in selected_game['children']:
        team_name = team['name']
        players = [player['name'] for player in team['children'] if 'data' in player]
        team_players[team_name] = players

    return render_template('select_players.html', game_name=game_name, team_players=team_players)

@app.route('/compare_players/<game_name>/<team1>/<player1>/<team2>/<player2>')
def compare_players(game_name, team1, player1, team2, player2):
    # Finding the selected game data
    selected_game = next((game for game in data['children'] if game['name'] == game_name), None)
    if not selected_game:
        return "Game not found", 404

    # Extracting player stats
    player1_stats = next((player['data'] for team in selected_game['children'] if team['name'] == team1
                          for player in team['children'] if player['name'] == player1), None)
    player2_stats = next((player['data'] for team in selected_game['children'] if team['name'] == team2
                          for player in team['children'] if player['name'] == player2), None)

    if not player1_stats or not player2_stats:
        return "Player not found", 404

    return render_template('compare_players.html', game_name=game_name, team1=team1, player1=player1, player1_stats=player1_stats,
                           team2=team2, player2=player2, player2_stats=player2_stats)


#This is part is for comparing team data
@app.route('/select_game_for_team', methods=['GET', 'POST'])
def select_game_for_team():
    if request.method == 'POST':
        selected_game = request.form.get('game')
        return redirect(url_for('select_quarter', game_name=selected_game))
    games = [game['name'] for game in data['children']]
    return render_template('select_game_for_team.html', games=games)


@app.route('/select_quarter/<game_name>', methods=['GET', 'POST'])
def select_quarter(game_name):
    if request.method == 'POST':
        selected_quarter = request.form.get('quarter')
        return redirect(url_for('display_comparison', game_name=game_name, quarter=selected_quarter))
    quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'OT']
    return render_template('select_quarter.html', game_name=game_name, quarters=quarters)

@app.route('/display_comparison/<game_name>/<quarter>')
def display_comparison(game_name, quarter):
    # Initialize a dict to hold the comparison data
    comparison_data = {}

    # Find the selected game
    selected_game = next((game for game in data['children'] if game['name'] == game_name), None)
    if not selected_game:
        return "Game not found", 404

    # Find and process the quarter data for each team
    for team in selected_game['children']:
        team_name = team['name']
        quarter_data = None
        for child in team['children']:
            if child['name'] == "Quarter Data" and quarter in child['data']:
                quarter_data = child['data'][quarter]
                break
        # Update to handle missing data: We add the data if it's there, or an empty dict if not
        comparison_data[team_name] = quarter_data if quarter_data else {}

    # Ensure that we have comparison data for at least one team
    if not any(comparison_data.values()):
        return f"{quarter} data not found for both teams", 404

    # Assign team names and extract data
    team1_name, team2_name = comparison_data.keys()
    team1_data = comparison_data[team1_name]
    team2_data = comparison_data[team2_name]

    # If one of the teams does not have data, we handle that elegantly in the chart creation
    fig = create_comparison_chart(team1_data, team2_data, team1_name, team2_name)

    # Convert the figures to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the display_comparison template with the graph
    return render_template('display_comparison.html', graphJSON=graphJSON, team1=team1_name, team2=team2_name)


def create_comparison_chart(team1_data, team2_data, team1_name, team2_name):
    
    stats_to_compare = ['PTS', 'AST', 'REB', 'STL', 'BLK']  
    fig = go.Figure()

    
    for stat in stats_to_compare:
        team1_stat_value = team1_data.get(stat, 0) 
        fig.add_trace(go.Bar(
            name=f'{team1_name} {stat}',
            x=[team1_stat_value],
            y=[stat],
            orientation='h',
            marker=dict(color='blue')
        ))


    for stat in stats_to_compare:
        team2_stat_value = team2_data.get(stat, 0)  
        fig.add_trace(go.Bar(
            name=f'{team2_name} {stat}',
            x=[-team2_stat_value],  
            y=[stat],
            orientation='h',
            marker=dict(color='red')
        ))

    
    fig.update_layout(barmode='overlay', title='Team Comparison by Stat')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
