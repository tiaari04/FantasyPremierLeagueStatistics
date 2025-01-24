# **Overview**

Developed a comprehensive Power BI dashboard to analyze Fantasy Premier League (FPL) player performance. The dashboard features interactive visuals, including:

* Top Performers: Identify the top 10 defenders, midfielders, forwards, and goalkeepers by points, goals, assists, and clean sheets.
* Price Efficiency: Visualize players' points-per-million performance with detailed insights.
* Best Picks: Identify the top 15 best players overall in the last 4 gameweeks based on total points, goals and assists
Key functionalities include automated data updates using Python scripts to fetch FPL data via APIs and store it in a PostgreSQL database for seamless integration with Power BI.

This project demonstrates skills in data extraction, transformation, and visualization to create actionable insights for FPL managers.

# **Technologies Used**

* Python:
Used for data extraction and automation scripts to fetch data from the FPL API.
Processed and stored player statistics, gameweek, and fixture data in the database.

* PostgreSQL:
Lightweight database to store FPL data, including player stats, team details, fixtures, and gameweeks.
Efficiently handled dynamic updates and queries for Power BI integration.

* Power BI:
Created interactive dashboards and visualizations for player performance and price efficiency metrics.
Enabled actionable insights with interactive filtering and drill-down options.

* FPL API:
Primary data source for retrieving real-time FPL statistics, including players, teams, and fixtures

* GitHub:
Hosted the Power BI report file and Python scripts for automation and reproducibility.

* JSON:
Managed data structures for API responses, enabling seamless parsing and transformation.

# **Installation and Setup**
1. Clone the Repository
```
git clone <repository-url>
cd FantasyPremierLeagueStatistics
```
2. Setup PoostgreSQL <br/>
Download and install PostgreSQL from the postgresql website, create a project and put in your credentials.
Put those same creadentials into the top of the files update_fpl.py, create_tables.py, and insert_data.py into the empty fields.
For example:
```
hostname = 'localhost' # since it's on your local computer
database = 'FPLstats'
username = 'postgres' # default
pwd = 'somepassword'
port_id = 5432
```

3. Run the python scripts <br/>
First install psycopg2
```
pip install psycopg2
```
Then in the termianl run these two commands to set up the tables
```
python create_tables.py
python insert_data.py
```

4. Lastly set up a task in task scheduler or run a cronjob to update the database using the file update_fpl.py.

5. I have example queries that I used for my PowerBI visuals listed under queries.txt and I have my PowerBI document listed as well. Use these as examples to build your own visuals!
My PowerBI Dashboard:
![image](https://github.com/user-attachments/assets/a70962a0-2696-4188-98e7-9ba07d7fc7aa)

# **Future Improvements**
* Adding different visuals to view different statistics like owned percentage and differential players.
