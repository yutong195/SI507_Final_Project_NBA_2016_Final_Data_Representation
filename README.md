# SI507_Final_Project_NBA_2016_Final_Data_Representation 

Running the code:
- For running the code, download the code to a local repository.
- If there is no data yet, create a folder with name “data” and run the `scraper.py`, which will scrawl the NBA 2016 final data online and save it as CSV files in the created folder.
- Then run the `construct_tree.py`. This code will read all the CSV files and construct the tree data structure to hold all the data.
- Finally, run the `data_vis_interaction.py` file and after it is running, copy and paste the local ip address (`http://127.0.0.1:5000`) to a search engine to open up the Flask app. The Flask app uses Plotly to visualize the data and enables several interesting interactions which would be introduced in the following content. You have to keep the python file running in order to open the online Flask app.
<br>

Data Structure:

- **Structure**
  - **TreeNode Class**: Represents a node in the tree. Each TreeNode has a name, an optional data dictionary, and a children list.
    - `add_child()`: Adds a new child node.
    - `display()`: Prints the tree structure, optionally with custom indentation and print function.
    - `to_dict()`: Converts the tree node (and its children) to a dictionary.
  - **Tree Creation**: The `create_nba_tree` function builds the tree. The root node represents the series, with child nodes for each game. Each game node has two children representing the teams, which in turn have children for quarter statistics and individual player statistics.

- **Data Representation:**
  - **Series Node**: The root node, named after the series (e.g., "NBA Finals 2016").
  - **Game Nodes**: Child nodes of the series, each representing a game in the series (e.g., "Game 1").
  - **Team Nodes**: Child nodes of each game, representing the competing teams (e.g., "Cavaliers", "Warriors").
    - **Quarter Data Node**: Contains quarter-by-quarter statistics for the team.
    - **Player Data Nodes**: Represent individual players with their game statistics.




