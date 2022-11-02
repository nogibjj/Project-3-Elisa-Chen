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

print(news_df)
