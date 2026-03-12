import requests
url = "http://localhost:8000/query_stockprice"
response = requests.post(url, json={"user_query": "平安银行最近20天的股价"})
price_info = response.json()['data']['response']
print(price_info)
