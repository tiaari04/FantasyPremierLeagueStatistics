import psycopg2

hostname = 'localhost'
database = 'FPLstats'
username = 'postgres'
pwd = 'jamPostGres04@'
port_id = 5432

connection = None
cursor = None

def create_tables():
    commands = (
        """
        CREATE TABLE teams (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            points INTEGER
        );
        """,
        """
        CREATE TABLE players (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        team INTEGER NOT NULL,
        position TEXT,
        price FLOAT,
        total_points INTEGER,
        ict FLOAT,
        most_transferred_in INTEGER,
        most_transferred_out INTEGER,
        owned_percentage FLOAT,
        FOREIGN KEY (team) REFERENCES teams(id)
        );
        """,
        """
        CREATE TABLE gameweeks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            deadline_time TEXT,
            finished BOOLEAN,
            is_current BOOLEAN,
            is_next BOOLEAN,
            is_previous BOOLEAN
        );
        """,
        """
        CREATE TABLE fixtures (
            id INTEGER PRIMARY KEY,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_difficulty INTEGER,
            away_difficulty INTEGER,
            FOREIGN KEY (home_team_id) REFERENCES teams(id),
            FOREIGN KEY (away_team_id) REFERENCES teams(id)
        );
        """,
        """
        CREATE TABLE player_stats (
            id SERIAL PRIMARY KEY,
            fixture_id INTEGER,
            player_id INTEGER,
            goals INTEGER,
            assists INTEGER,
            FOREIGN KEY (fixture_id) REFERENCES fixtures(id),
            FOREIGN KEY (player_id) REFERENCES players(id)
        );
        """
    )
    for command in commands:
        cursor.execute(command)

    cursor.close()
    connection.commit()
    print("done")

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
    # finally:
    #     if cursor is not None:
    #         cursor.close()
    #     if connection is not None:
    #         connection.close()

def main():
    connect()
    create_tables()

    connection.close()

if __name__ == "__main__":
    main()