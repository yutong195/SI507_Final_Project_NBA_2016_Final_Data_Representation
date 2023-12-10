import numpy as np
import pandas as pd
import json


class TreeNode:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def display(self, indent=0, custom_print=print):
        custom_print(' ' * indent + self.name)
        if self.data is not None:
            for key, value in self.data.items():
                custom_print(' ' * (indent + 2) + f"{key}: {value}")
        for child in self.children:
            child.display(indent + 2, custom_print)

    def to_dict(self):
        node_dict = {"name": self.name}
        if self.data is not None:
            node_dict["data"] = self.data
        if self.children:
            node_dict["children"] = [child.to_dict() for child in self.children]
        return node_dict

# Function to create a tree structure for NBA game data
def create_nba_tree(series_name, games_data):
    # Root node
    series_tree = TreeNode(series_name)

    # Adding games as child nodes
    for game_number, game in enumerate(games_data, start=1):
        game_node = TreeNode(f"Game {game_number}")

        # Adding team data as child nodes of each game
        for team, team_data in game.items():
            team_node = TreeNode(team)

            # Team quarter data
            team_quarter_data = {row['Qtr']: row.drop('Qtr').to_dict() for _, row in team_data['team_quarter_data'].iterrows()}
            team_quarter_node = TreeNode("Quarter Data", team_quarter_data)
            team_node.add_child(team_quarter_node)

            # Player data
            # Player data
            for _, player in team_data['player_data'].iterrows():
                player_dict = player.to_dict()
                # Adjust the dictionary as needed, for example, removing or renaming keys
                player_name = player_dict.pop('Player')  # Extract and remove 'Player' key
                player_node = TreeNode(player_name, player_dict)
                team_node.add_child(player_node)

            game_node.add_child(team_node)

        series_tree.add_child(game_node)

    return series_tree

# Function to read data from a CSV file
def read_csv(file_path):
    return pd.read_csv(file_path)

# Create a tree structure for the two games
games_data = [
    {
        "Cavaliers": {
            
            "team_quarter_data": read_csv('data/g1_cav_team_data.csv'),
            "player_data": read_csv('data/g1_cav_player_data.csv')
        },
        "Warriors": {
            "team_quarter_data": read_csv('data/g1_war_team_data.csv'),
            "player_data": read_csv('data/g1_war_player_data.csv')
        }
    },
    {
        "Cavaliers": {
            "team_quarter_data": read_csv('data/g2_cav_team_data.csv'),
            "player_data": read_csv('data/g2_cav_player_data.csv')
        },
        "Warriors": {
            "team_quarter_data": read_csv('data/g2_war_team_data.csv'),
            "player_data": read_csv('data/g2_war_player_data.csv')
        }
    },
    {
        "Cavaliers": {
            "team_quarter_data": read_csv('data/g3_cav_team_data.csv'),
            "player_data": read_csv('data/g3_cav_player_data.csv')
        },
        "Warriors": {
            "team_quarter_data": read_csv('data/g3_war_team_data.csv'),
            "player_data": read_csv('data/g3_war_player_data.csv')
        }
    },
    {
        "Cavaliers": {
            "team_quarter_data": read_csv('data/g4_cav_team_data.csv'),
            "player_data": read_csv('data/g4_cav_player_data.csv')
        },
        "Warriors": {
            "team_quarter_data": read_csv('data/g4_war_team_data.csv'),
            "player_data": read_csv('data/g4_war_player_data.csv')
        }
    },
    {
        "Cavaliers": {
            "team_quarter_data": read_csv('data/g5_cav_team_data.csv'),
            "player_data": read_csv('data/g5_cav_player_data.csv')
        },
        "Warriors": {
            "team_quarter_data": read_csv('data/g5_war_team_data.csv'),
            "player_data": read_csv('data/g5_war_player_data.csv')
        }
    },
    {
        "Cavaliers": {
            "team_quarter_data": read_csv('data/g6_cav_team_data.csv'),
            "player_data": read_csv('data/g6_cav_player_data.csv')
        },
        "Warriors": {
            "team_quarter_data": read_csv('data/g6_war_team_data.csv'),
            "player_data": read_csv('data/g6_war_player_data.csv')
        }
    },
    {
        "Cavaliers": {
            "team_quarter_data": read_csv('data/g7_cav_team_data.csv'),
            "player_data": read_csv('data/g7_cav_player_data.csv')
        },
        "Warriors": {
            "team_quarter_data": read_csv('data/g7_war_team_data.csv'),
            "player_data": read_csv('data/g7_war_player_data.csv')
        }
    }
]

nba_finals_tree = create_nba_tree("NBA Finals 2016", games_data)

nba_finals_dict = nba_finals_tree.to_dict()

# Convert to JSON and write to file
with open('nba_finals_tree.json', 'w', encoding='utf-8') as file:
    json.dump(nba_finals_dict, file, ensure_ascii=False, indent=4)

with open('output.txt', 'w',encoding='utf-8') as file:
    def custom_print(data):
        print(data, file=file)
    nba_finals_tree.display(custom_print=custom_print)