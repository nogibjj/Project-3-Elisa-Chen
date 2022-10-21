import sqlite3
import csv
import pandas as pd
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to a SQLite database in Python"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("database connection created!")
    except Error as e:
        print(e)
    return conn


def create_table(c, create_table_sql):
    """create a table from the create_table_sql statement"""
    try:
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def add_data_to_db(cur, filename, db_name, num_cols):
    """add data from csv file to database"""
    file = open(filename, encoding="utf8")
    contents = csv.reader(file)
    questionmarks = ", ".join("?" * num_cols)
    insert_records = "INSERT INTO " + db_name + " VALUES " + "(" + questionmarks + ")"
    cur.executemany(insert_records, contents)


if __name__ == "__main__":
    db_connection = create_connection(r"./sqlite/db/database.db")
    cursor = db_connection.cursor()
    create_table(
        cursor,
        """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY, 
                                name TEXT, 
                                age INTEGER, 
                                email TEXT);""",
    )
    cursor.execute(
        "DELETE FROM users;",
    )
    add_data_to_db(cursor, "people.csv", "users", 4)

    # querying the database
    query = "SELECT * FROM users"
    rows = cursor.execute(query).fetchall()
    # for row in rows:
    #    print(row)

    # store it in a pandas dataframe
    surveys_df = pd.read_sql_query("SELECT * from users", db_connection)
    print(surveys_df)

    db_connection.commit()
    db_connection.close()