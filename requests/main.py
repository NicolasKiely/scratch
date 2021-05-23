import requests
import pandas

API_URL = "https://api.pro.coinbase.com"
CURRENCIES_PATH = "/currencies"

response = requests.get(API_URL + CURRENCIES_PATH)
data = response.json()

currencies_df = pandas.DataFrame.from_records(data)
currencies_df.to_csv("currencies.csv", index=False)
