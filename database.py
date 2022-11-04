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


def add_data_to_db(cur, filename, db_name, num_cols, enc="utf-8"):
    """add data from csv file to database"""
    file = open(filename, encoding=enc)
    contents = csv.reader(file)
    #delete header from csv file
    next(contents)
    questionmarks = ", ".join("?" * num_cols)
    colnames = "(" + ','.join([item[0] for item in cur.execute("SELECT * FROM " + db_name + " LIMIT 1").description[1:]]) + ")"
    insert_records = "INSERT INTO " + db_name + colnames + " VALUES " + "(" + questionmarks + ")"
    cur.executemany(insert_records, contents)
    print("data added to database!")    

def modify_table(path, q):
    """modify table with a new query"""
    db_conn = create_connection(path)
    cur = db_connection.cursor()
    cur.execute(q)
    print("table modified!")
    db_conn.commit()
    db_conn.close()

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