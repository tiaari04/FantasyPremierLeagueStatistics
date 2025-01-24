import psycopg2
import requests
from datetime import datetime, timezone, timedelta

hostname = ''
database = ''
username = ''
pwd = ''
port_id = 5

connection = None
cursor = None

def connect():
    global connection, cursor
    try:
        connection = psycopg2.connect(host = hostname,
                                dbname = database,
                                user = username,
                                password = pwd,
                                port = port_id)
        
        cursor = connection.cursor()
        print("working")

    except Exception as error:
        print(error)

def pos_number_to_word(position_number):
    if position_number == 1:
        return "GOALKEEPER"
    elif position_number == 2:
        return "DEFENDER"
    elif position_number == 3:
        return "MIDFIELDER"
    elif position_number == 4:
        return "FORWARD"


def insert_into_players():
    global connection, cursor
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url).json()

    for player in response["elements"]:

        cursor.execute("""
        SELECT COUNT(*)
        FROM players
        WHERE id = %s
        """, (player["id"],))
        exists = cursor.fetchone()[0]
        
        if exists:
            cursor.execute("""
                UPDATE players
                SET price = %s, assists = %s, total_points = %s, goals_scored = %s, clean_sheets = %s, ict = %s, most_transferred_in = %s, most_transferred_out = %s, owned_percentage = %s
                WHERE id = %s
            """, (player["now_cost"] / 10, player["assists"], player["total_points"], player["goals_scored"],
                player["clean_sheets"], player["ict_index"], player["transfers_in_event"], player["transfers_out_event"], 
                player["selected_by_percent"], player["id"]))
        else:
            cursor.execute("""
                INSERT INTO players (id, name, team, position, price, total_points, goals_scored, assists, clean_sheets, ict, most_transferred_in, most_transferred_out, owned_percentage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (player["id"], player["web_name"], player["team"], pos_number_to_word(player["element_type"]), player["now_cost"] / 10, player["total_points"], 
                player["goals_scored"], player["assists"], player["clean_sheets"], player["ict_index"], player["transfers_in_event"], player["transfers_out_event"], 
                player["selected_by_percent"]))

    connection.commit()

def insert_into_teams():
    global connection, cursor
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url).json()

    for team in response["teams"]:
        cursor.execute("""
        SELECT COUNT(*)
        FROM teams
        WHERE id = %s
        """, (team["id"],))
        exists = cursor.fetchone()[0]

        if exists:
            cursor.execute("""
                UPDATE teams
                SET points = %s
                WHERE id = %s
            """, (team["points"], team["id"]))

        else:
            cursor.execute("""
                INSERT INTO teams (id, name, points)
                VALUES (%s, %s, %s);
            """, (team["id"], team["name"], team["points"]))

    connection.commit()

def insert_into_gameweeks():
    global connection, cursor
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url).json()

    for gameweek in response["events"]:

        cursor.execute("""
        SELECT COUNT(*)
        FROM gameweeks
        WHERE id = %s
        """, (gameweek["id"],))
        exists = cursor.fetchone()[0]

        if exists:
            cursor.execute("""
                UPDATE gameweeks
                SET deadline_time = %s, finished = %s, is_current = %s, is_next = %s, is_previous = %s
                WHERE id = %s
            """, (gameweek["deadline_time"], gameweek["finished"], gameweek["is_current"], 
                gameweek["is_next"], gameweek["is_previous"], gameweek["id"]))

        else:
            cursor.execute("""
                INSERT INTO gameweeks (id, name, deadline_time, finished, is_current, is_next, is_previous)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (gameweek["id"], gameweek["name"], gameweek["deadline_time"], gameweek["finished"], gameweek["is_current"], 
                gameweek["is_next"], gameweek["is_previous"]))

    connection.commit()

def insert_into_fixtures():
    global connection, cursor
    url = "https://fantasy.premierleague.com/api/fixtures/"
    fixtures = requests.get(url).json()

    for fixture in fixtures:
        cursor.execute("""
        SELECT COUNT(*)
        FROM fixtures
        WHERE id = %s
        """, (fixture["id"],))
        exists = cursor.fetchone()[0]

        if exists:
            cursor.execute("""
                UPDATE fixtures
                SET home_team_id = %s, away_team_id = %s, home_difficulty = %s, away_difficulty = %s, gameweek_id = %s
                WHERE id = %s
            """, (fixture["team_h"], fixture["team_a"], fixture["team_h_difficulty"],
              fixture["team_a_difficulty"], fixture["event"], fixture["id"]))
        
        else:
            cursor.execute("""
                INSERT INTO fixtures (id, home_team_id, away_team_id, home_difficulty, away_difficulty, gameweek_id)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (fixture["id"], fixture["team_h"], fixture["team_a"], fixture["team_h_difficulty"],
                fixture["team_a_difficulty"], fixture["event"]))

    connection.commit()

def insert_into_player_stats():
    global connection, cursor
    url = "https://fantasy.premierleague.com/api/fixtures/"
    fixtures = requests.get(url).json()

    for fixture in fixtures:
        fixture_id = fixture["id"]
        stats = fixture.get("stats", [])
        
        for stat_entry in stats:
            stat_type = stat_entry.get("identifier")  # The key indicating the type of stat
            
            # Process both "away" (a) and "home" (h) players
            for location in ["a", "h"]:
                players = stat_entry.get(location, [])
                
                if stat_type == "goals_scored":
                    for player_stat in players:
                        player_id = player_stat["element"]
                        goals = player_stat["value"]

                        cursor.execute("""
                        SELECT COUNT(*)
                        FROM player_stats
                        WHERE fixture_id = %s AND player_id = %s
                        """, (fixture_id, player_id))
                        exists = cursor.fetchone()[0]

                        if exists:
                            # Update if the row exists
                            cursor.execute("""
                            UPDATE player_stats
                            SET goals = %s
                            WHERE fixture_id = %s AND player_id = %s
                            """, (goals, fixture_id, player_id))
                        else:
                            cursor.execute("""
                            INSERT INTO player_stats (fixture_id, player_id, goals, assists)
                            VALUES (%s, %s, %s, %s)
                            """, (fixture_id, player_id, goals, 0))  # 0 assists as placeholder

                elif stat_type == "assists":
                    for player_stat in players:
                        player_id = player_stat["element"]
                        assists = player_stat["value"]

                        cursor.execute("""
                        SELECT COUNT(*)
                        FROM player_stats
                        WHERE fixture_id = %s AND player_id = %s
                        """, (fixture_id, player_id))
                        exists = cursor.fetchone()[0]

                        if exists:
                            # Update if the row exists
                            cursor.execute("""
                            UPDATE player_stats
                            SET assists = %s
                            WHERE fixture_id = %s AND player_id = %s
                            """, (assists, fixture_id, player_id))
                        else:
                            # Insert if the row does not exist
                            cursor.execute("""
                            INSERT INTO player_stats (fixture_id, player_id, goals, assists)
                            VALUES (%s, %s, %s, %s)
                            """, (fixture_id, player_id, 0, assists))  # 0 goals as placeholder

    connection.commit()

def update():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url).json()
    gameweeks = response["events"]

    # Get current date
    current_date = datetime.now(timezone.utc)

    for gw in gameweeks:
        deadline = datetime.strptime(gw["deadline_time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if deadline - timedelta(days=1) <= current_date <= deadline + timedelta(days=1):
            print(f"Updating data for Gameweek {gw['id']}")
            insert_into_teams()
            insert_into_players()
            insert_into_gameweeks()
            insert_into_fixtures()
            insert_into_player_stats()

            break

def main():
    connect()
    update()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()