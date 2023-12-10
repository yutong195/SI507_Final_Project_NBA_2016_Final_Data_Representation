import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# The URL of the page you want to scrape
#url = 'https://www.basketball-reference.com/boxscores/202304160PHO.html'

def get_player_data(url, desired_table_index):
    # Send a GET request to the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find all tables on the page
        tables = soup.find_all('table')

        # Loop through all found tables and print out their summaries or a small part of them
        # This is to help identify the table you're interested in
        # for i, table in enumerate(tables):
        #     # Convert the table to a dataframe
            # df = pd.read_html(str(table))[0]
        #     # Print out the first few rows of the dataframe
        #     print(f"Table {i}:")
        #     print(df.head(10))
        #     print("\n")
            # Once you have identified the table you are interested in, you can use its index to select it
        # For example, if the table you want is the third table on the page:
        df = pd.read_html(str(tables[desired_table_index]))[0]
        # Remove the first row (multi-level header)
        df.columns = df.columns.get_level_values(1)  # Use the second level of multi-index as the columns

        # Rename the first column to "Player"
        df.columns.values[0] = "Player"

        # Drop the fifth row (index 4 after dropping the header row)
        df = df.drop(df.index[5])
        return df
    
    else:
        print(f"Failed to retrieve content, status code: {response.status_code}")

def get_team_data(url, desired_table_index):
    # Send a GET request to the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find all tables on the page
        tables = soup.find_all('table')

        # Loop through all found tables and print out their summaries or a small part of them
        # This is to help identify the table you're interested in
        # for i, table in enumerate(tables):
        #     # Convert the table to a dataframe
            # df = pd.read_html(str(table))[0]
        #     # Print out the first few rows of the dataframe
        #     print(f"Table {i}:")
        #     print(df.head(10))
        #     print("\n")
            # Once you have identified the table you are interested in, you can use its index to select it
        # For example, if the table you want is the third table on the page:
        df = pd.read_html(str(tables[desired_table_index]))[0]
        return df
    
    else:
        print(f"Failed to retrieve content, status code: {response.status_code}")
'''
#Game 1 data caching process
#Caching the g1 warriors data
g1_war_player = get_player_data("https://www.basketball-reference.com/boxscores/201606020GSW.html",8)
g1_war_player.to_csv('data/g1_war_player_data.csv', index=False)

#Caching the g1 cavaliers data
g1_cav_player = get_player_data("https://www.basketball-reference.com/boxscores/201606020GSW.html",0)
#print(df_wc_r1_g1_suns_player)
g1_cav_player.to_csv('data/g1_cav_player_data.csv', index=False)


g1_cav_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606020GSW.html",0)
print(g1_cav_team)
g1_cav_team.to_csv('data/g1_cav_team_data.csv', index=False)


g1_war_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606020GSW.html",1)
print(g1_war_team)
g1_war_team.to_csv('data/g1_war_team_data.csv', index=False)

#Caching game2 data
#Caching the g2 warriors data
g2_war_player = get_player_data("https://www.basketball-reference.com/boxscores/201606050GSW.html",8)
g2_war_player.to_csv('data/g2_war_player_data.csv', index=False)

#Caching the g2 cavaliers data
g2_cav_player = get_player_data("https://www.basketball-reference.com/boxscores/201606050GSW.html",0)
#print(df_wc_r1_g1_suns_player)
g2_cav_player.to_csv('data/g2_cav_player_data.csv', index=False)

#Caching the g2 cavaliers team data
g2_cav_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606050GSW.html",0)
print(g2_cav_team)
g2_cav_team.to_csv('data/g2_cav_team_data.csv', index=False)

#Caching the g2 warriors team data
g2_war_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606050GSW.html",1)
print(g2_war_team)
g2_war_team.to_csv('data/g2_war_team_data.csv', index=False)
'''

#Caching game3 data
#Caching the g3 warriors data
g3_war_player = get_player_data("https://www.basketball-reference.com/boxscores/201606080CLE.html",0)
g3_war_player.to_csv('data/g3_war_player_data.csv', index=False)

#Caching the g3 cavaliers data
g3_cav_player = get_player_data("https://www.basketball-reference.com/boxscores/201606080CLE.html",8)
g3_cav_player.to_csv('data/g3_cav_player_data.csv', index=False)

#Caching the g3 cavaliers team data
g3_cav_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606080CLE.html",1)
g3_cav_team.to_csv('data/g3_cav_team_data.csv', index=False)

#Caching the g3 warriors team data
g3_war_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606080CLE.html",0)
g3_war_team.to_csv('data/g3_war_team_data.csv', index=False)



#Caching game4 data
#Caching the g4 warriors data
g4_war_player = get_player_data("https://www.basketball-reference.com/boxscores/201606100CLE.html",0)
g4_war_player.to_csv('data/g4_war_player_data.csv', index=False)

#Caching the g4 cavaliers data
g4_cav_player = get_player_data("https://www.basketball-reference.com/boxscores/201606100CLE.html",8)
g4_cav_player.to_csv('data/g4_cav_player_data.csv', index=False)

#Caching the g4 cavaliers team data
g4_cav_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606100CLE.html",1)
g4_cav_team.to_csv('data/g4_cav_team_data.csv', index=False)

#Caching the g4 warriors team data
g4_war_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606100CLE.html",0)
g4_war_team.to_csv('data/g4_war_team_data.csv', index=False)
'''
'''
'''
#Caching game5 data
#Caching the g5 warriors data
g5_war_player = get_player_data("https://www.basketball-reference.com/boxscores/201606130GSW.html",8)
g5_war_player.to_csv('data/g5_war_player_data.csv', index=False)

#Caching the g5 cavaliers data
g5_cav_player = get_player_data("https://www.basketball-reference.com/boxscores/201606130GSW.html",0)
g5_cav_player.to_csv('data/g5_cav_player_data.csv', index=False)

#Caching the g5 cavaliers team data
g5_cav_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606130GSW.html",0)
g5_cav_team.to_csv('data/g5_cav_team_data.csv', index=False)

#Caching the g5 warriors team data
g5_war_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606130GSW.html",1)
g5_war_team.to_csv('data/g5_war_team_data.csv', index=False)
'''


#Caching game6 data
#Caching the g6 warriors data
g6_war_player = get_player_data("https://www.basketball-reference.com/boxscores/201606160CLE.html",0)
g6_war_player.to_csv('data/g6_war_player_data.csv', index=False)

#Caching the g6 cavaliers data
g6_cav_player = get_player_data("https://www.basketball-reference.com/boxscores/201606160CLE.html",8)
g6_cav_player.to_csv('data/g6_cav_player_data.csv', index=False)

#Caching the g6 cavaliers team data
g6_cav_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606160CLE.html",1)
g6_cav_team.to_csv('data/g6_cav_team_data.csv', index=False)

#Caching the g6 warriors team data
g6_war_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606160CLE.html",0)
g6_war_team.to_csv('data/g6_war_team_data.csv', index=False)


'''
#Caching game7 data
#Caching the g7 warriors data
g7_war_player = get_player_data("https://www.basketball-reference.com/boxscores/201606190GSW.html",8)
g7_war_player.to_csv('data/g7_war_player_data.csv', index=False)

#Caching the g7 cavaliers data
g7_cav_player = get_player_data("https://www.basketball-reference.com/boxscores/201606190GSW.html",0)
g7_cav_player.to_csv('data/g7_cav_player_data.csv', index=False)

#Caching the g7 cavaliers team data
g7_cav_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606190GSW.html",0)
g7_cav_team.to_csv('data/g7_cav_team_data.csv', index=False)

#Caching the g7 warriors team data
g7_war_team = get_team_data("https://www.basketball-reference.com/boxscores/shot-chart/201606190GSW.html",1)
g7_war_team.to_csv('data/g7_war_team_data.csv', index=False)
'''


'''
response = requests.get("https://www.basketball-reference.com/boxscores/shot-chart/201606020GSW.html")

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find all tables on the page
    tables = soup.find_all('table')

    # Loop through all found tables and print out their summaries or a small part of them
    # This is to help identify the table you're interested in
    for i, table in enumerate(tables):
        # Convert the table to a dataframe
        df = pd.read_html(str(table))[0]
        # Print out the first few rows of the dataframe
        print(f"Table {i}:")
        print(df.head(10))
        print("\n")
'''