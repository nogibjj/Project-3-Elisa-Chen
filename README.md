# Project-3-Elisa-Chen - News Neutrality Classifier

This repository contains the source code, config files and a short video demo of my project on detecting biasness in news. 

![Project-3-Diagram](https://user-images.githubusercontent.com/25168588/199878167-2d7683ec-1a5c-4432-ae1f-a73e6d7e99d4.png)

## Key Objectives and Project Description
The reliability of news sources is becoming a major concern for the public. Understanding the biasness of various news sources can help the public make better informed decisions about which news sources to trust. In this project, I use a [Bert Based Text Classifier](https://huggingface.co/cffl/bert-base-styleclassification-subjective-neutral?text=I+like+you.+I+love+you) from Hugging Face to determine the degree of biasness of articles posted by [The Guardian News](https://www.theguardian.com/us).

This project was created as part of the Data Engineering class IDS 706 at Duke. The objective of the project was to create a useful SQL script that queries from a database. 

## Demo Video

## Methodology
1. [News data](https://www.kaggle.com/datasets/sunnysai12345/news-summary) was downloaded from Kaggle.
2. The news data was stored in a new table in a SQLite database
3. The news data was cleaned and queried with SQL
4. The Hugging Face classifer was applied to the query results and the table was updated with bias_classification and scores
5. The final results were queried from the updated table using SQL

## User Instructions

### Data Files
All source data files are stored under the directory `data`. The database for the news data is stored in `sqlite/news_data.db`. 

### Helper Functions
`database.py`: helper functions for database management (creating tables, adding data to a table from csv etc.)

`import_news_data.py`: script to upload news data to a table called `news` in the `news_data` database

`classification_script.py`: script to apply classifier to query results and return a new SQL query with the aggregated results

## Results
Based on the data, we can observe that over one third of the articles written in the Guardian between the timeperiod 2016-2017 were considered to have subjective clauses, which raises questions about the objectivity of the Guardian articles written during the timeperiod. 

Further investigation could've been done by fine-tuning the model with better training data (news specific data) and tagging the clauses that were considered the most subjective in each article to understand the nature of subjectivity in news articles.

| Bias Classification | Count | % of Total |
| ----------- | ----------- | ----------- |
| Neutral      | 190       | 69.85        |
| Subjective   | 82       | 30.15       |

