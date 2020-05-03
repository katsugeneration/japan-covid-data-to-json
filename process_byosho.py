import json
import pandas as pd
import requests
res = requests.get('https://www.stopcovid19.jp/data/bedforinfection_summary.json', allow_redirects=True)
with open('bedforinfection_summary.json', 'wb') as f:
  f.write(res.content)
res.close()


with open('bedforinfection_summary.json', 'r') as f:
  data = json.load(f)
df_byosho = pd.read_json(json.dumps(data['area']), orient='records')
df_byosho = df_byosho.set_index(df_byosho['name_ja'])

df_byosho_open = pd.read_csv('https://www.stopcovid19.jp/data/bedforinfection_current.csv', header=0)
df_byosho_open = df_byosho_open.sort_values(by='発表日')
df_byosho_open = df_byosho_open.groupby('自治体名').last()

df_p_now = pd.read_csv('https://www.stopcovid19.jp/data/covid19japan.csv', header=0)
df_p_now = df_p_now.set_index(df_p_now['name_jp'])

columns = df_p_now.index.tolist()
df = pd.DataFrame(index=['patients', 'beds'], columns=columns)

for c in columns:
  try:
    beds = df_byosho_open.loc[c, '新型コロナウイルス対策感染症病床数']
  except:
    beds = df_byosho.loc[c, 'sum'] + df_byosho.loc[c, 'sumk']
  df[c]['patients'] = df_p_now.loc[c, 'ncurrentpatients']
  df[c]['beds'] = beds

df.to_json('byosho.json', orient='index')