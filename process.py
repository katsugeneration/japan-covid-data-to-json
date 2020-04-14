import pandas as pd

df = pd.read_csv('https://dl.dropboxusercontent.com/s/6mztoeb6xf78g5w/COVID-19.csv', header=0)
df = df.pivot_table(
    values='人数',
    index=pd.to_datetime(df['確定日'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d'),
    columns='受診都道府県',
    aggfunc='sum',
    fill_value=0)
df = df.cumsum()
print(df)
print(df.sum(axis=1))
df.to_json('covid.json', orient='index')
