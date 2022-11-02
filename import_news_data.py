from database import create_connection, create_table, add_data_to_db
import pandas as pd
from datasets import Dataset

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
                                headlines TEXT,
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

def return_hf_dataset(path, query):
    """Return a HuggingFace Dataset object"""
    db_connection = create_connection(path)
    df = pd.read_sql_query(query, db_connection)
    db_connection.close()
    return Dataset.from_pandas(df)

def return_pd_dataset(path, query):
    """Return a pandas dataframe"""
    db_connection = create_connection(path)
    df = pd.read_sql_query(query, db_connection)
    db_connection.close()
    return df

if __name__ == "__main__":
    #main()
    db_connection_news = create_connection(r"./sqlite/db/news_data.db")
    cursor_news = db_connection_news.cursor()
    
    query_news = """SELECT 
    CASE WHEN author IS NULL THEN 'Unknown' ELSE author END AS author
    ,SUBSTR(date,0,12) as date
    ,lower(beadlines) as headlines
    ,lower(text) as text
    ,SUBSTR(URL, INSTR(URL, '://' ) + 3, MAX(INSTR(URL, '.com/'), INSTR(URL, '.in/')) - INSTR(URL, '://') + 1) as domain
    FROM news
    WHERE SUBSTR(URL, INSTR(URL, '://' ) + 3, MAX(INSTR(URL, '.com/'), INSTR(URL, '.in/')) - INSTR(URL, '://') + 1) like '%theguardian%'
    ORDER BY date DESC
    ;
    """
    #query_news = """SELECT * FROM news LIMIT 20"""
    #query_from_news(cursor_news, query_news)

    news_df = pd.read_sql_query(query_news, db_connection_news)
    print(len(news_df))

    db_connection_news.close()

    # return HF dataset
    hf_news_dataset = return_hf_dataset(r"./sqlite/db/news_data.db", query_news)
