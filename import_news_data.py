from database import create_connection, create_table, add_data_to_db

def main():
    """A script to ingest the news data to a new database called news_data.
    
    Please see more details about data here: https://www.kaggle.com/datasets/sunnysai12345/news-summary
    """
    db_connection = create_connection(r"./sqlite/db/news_data.db")
    cursor = db_connection.cursor()

    create_table(
        cursor,
        """CREATE TABLE IF NOT EXISTS news (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                author TEXT, 
                                date DATE,
                                beadlines TEXT,
                                URL TEXT,
                                text TEXT,
                                ctext TEXT);""",
    )

    add_data_to_db(cursor, "./data/news_summary.csv", "news", 6, "ISO-8859-1")

    db_connection.commit()
    db_connection.close()

def query_from_news(cursor, query):
    """Query from news database"""
    rows = cursor.execute(query).fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    #main()
    db_connection = create_connection(r"./sqlite/db/news_data.db")
    cursor = db_connection.cursor()
    query = """SELECT COUNT(*) FROM news"""
    query_from_news(cursor, query)