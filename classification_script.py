from transformers import pipeline
from import_news_data import return_pd_dataset
from database import add_data_to_db
import sqlite3
import pandas as pd

classify = pipeline(
    task="text-classification",
    model="cffl/bert-base-styleclassification-subjective-neutral",
    top_k=1,
)

query = """SELECT 
    CASE WHEN author IS NULL THEN 'Unknown' ELSE author END AS author
    ,SUBSTR(date,0,12) as date
    ,lower(beadlines) as headlines
    ,SUBSTR(URL, INSTR(URL, '://' ) + 3, MAX(INSTR(URL, '.com/'), INSTR(URL, '.in/')) - INSTR(URL, '://') + 1) as domain
    ,lower(text) as text
    ,lower(ctext) as ctext
    FROM news
    WHERE SUBSTR(URL, INSTR(URL, '://' ) + 3, MAX(INSTR(URL, '.com/'), INSTR(URL, '.in/')) - INSTR(URL, '://') + 1) like '%theguardian%'
    ORDER BY date DESC
    ;
    """

news_df = return_pd_dataset(r"./sqlite/db/news_data.db", query)

#identify the biasness of the text for each row
news_df['bias_classification'] = news_df['text'].apply(lambda x: classify(x)[0][0]['label'])
news_df['score'] = news_df['text'].apply(lambda x: classify(x)[0][0]['score'])

add_bias_col_q = """ALTER TABLE news ADD COLUMN bias_classification TEXT IF NOT EXISTS;"""
add_score_col_q = """ALTER TABLE news ADD COLUMN score REAL IF NOT EXISTS;"""
truncate_query = """DELETE FROM news;"""

#save the dataframe to a csv file
news_df.to_csv(r'./data/news_summary_bias.csv', index = False)

conn = sqlite3.connect(r"./sqlite/db/news_data.db")
c = conn.cursor()
#c.execute(add_bias_col_q)
#c.execute(add_score_col_q)
c.execute(truncate_query)

add_data_to_db(c, "./data/news_summary_bias.csv", "news", 8)

query_news= """SELECT bias_classification
, count(*) as count 
, round(count(*)*100.0/(select count(*) from news),2) as percentage_of_total
FROM news GROUP BY bias_classification;"""

df_updated = pd.read_sql_query(query_news, conn)
print(df_updated)
print(len(df_updated))

#close the connection
conn.close()
