import requests
import time
import pandas as pd

def get_all_indicatiors(page=1):
    url = 'http://api.worldbank.org/v2/indicators?format=json&page={}'.format(page)
    print('GET: ' + url)
    return requests.get(url).json()

def append_data(df, json_response):
    new_data = [{ 'Indicator': json_response[1][i]['id'], 'Name':json_response[1][i]['name']} for i in range(len(json_response[1]))]
    df = df.append(new_data)
    return df

indicators_df = pd.DataFrame(columns=['Indicator', 'Name'])

json_response = get_all_indicatiors()
indicators_df = append_data(indicators_df, json_response)
pages_count = json_response[0]['pages']

for page in range(2, pages_count+1):
    json_response = get_all_indicatiors(page)
    indicators_df = append_data(indicators_df, json_response)
    time.sleep(1)

indicators_df.to_csv('indicators.tsv', sep='\t', index=False)
