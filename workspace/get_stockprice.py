import requests

def query(user_query):
    url = "http://localhost:8000/query_stockprice"
    payload = {
        "user_query": user_query
    }
    response = requests.post(url, json=payload)
    return response.json()['data']['response']

# 调用 query 函数查询平安银行最近20天股价
result = query("平安银行最近20天股价")
print(result)
