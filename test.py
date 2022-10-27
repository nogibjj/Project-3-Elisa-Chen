from database import create_connection

def test_news_database():
    """Testing that the num of news records is up to date"""
    db_connection_news = create_connection(r"./sqlite/db/news_data.db")
    cursor_news = db_connection_news.cursor()
    query_news = """SELECT COUNT(*) FROM news"""
    rows = cursor_news.execute(query_news).fetchall()
    assert rows[0][0] == 4514
    db_connection_news.close()