#!/usr/bin/env python3
import http.client
import json

conn = http.client.HTTPConnection("localhost", 8000)
headers = {'Content-type': 'application/json'}
data = json.dumps({"user_query": "平安银行最近20天的股价"})
conn.request("POST", "/query_stockprice", data, headers)
response = conn.getresponse()
result = response.read().decode()
print(result)

# 解析结果
data = json.loads(result)
price_info = data['data']['response']
print("\n=== 平安银行最近20天股价信息 ===")
print(price_info)
