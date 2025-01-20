import psycopg2

hostname = 'localhost'
database = 'FPLstats'
username = 'postgres'
pwd = 'jamPostGres04@'
port_id = 5432

connection = None
cursor = None

def connect():
    path = "C:\Program Files\PostgreSQL\17\data\base\16396"

    global connection, cursor
    try:
        connection = psycopg2.connect(host = hostname,
                                dbname = database,
                                user = username,
                                password = pwd,
                                port = port_id)
        
        cursor = connection.cursor()

    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def main():
    global connection, cursor
    connect()

if __name__ == "__main__":
    main()