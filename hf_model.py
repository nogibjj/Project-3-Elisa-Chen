from transformers import pipeline
from import_news_data import return_pd_dataset

classify = pipeline(
    task="text-classification",
    model="cffl/bert-base-styleclassification-subjective-neutral",
    top_k=1,
)

query = """SELECT 
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

news_df = return_pd_dataset(r"./sqlite/db/news_data.db", query)

#identify the biasness of the text for each row
news_df['bias_classification'] = news_df['text'].apply(lambda x: classify(x)[0][0]['label'])
news_df['score'] = news_df['text'].apply(lambda x: classify(x)[0][0]['score'])

#-----------------------------
#DOUBLE CHECK THIS AND ALSO MOVE TO DATABASE.PY FILE

#save the dataframe to a csv file
news_df.to_csv(r'./data/news_summary_bias.csv', index = False)

#update the database with the bias classification
import sqlite3
import pandas as pd

conn = sqlite3.connect(r"./sqlite/db/news_data.db")
c = conn.cursor()

#read the csv file
df = pd.read_csv(r'./data/news_summary_bias.csv')

#insert the bias classification into the database
df.to_sql('news', conn, if_exists='replace', index = False)

#close the connection
conn.close()
