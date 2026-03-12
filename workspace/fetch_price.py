import sys
sys.path.insert(0, '/skills/stockprice')
from query import query

result = query("平安银行最近20天股价")
with open('/workspace/price_result.txt', 'w', encoding='utf-8') as f:
    f.write(result)

# 同时打印结果
print("=" * 50)
print("平安银行最近20天股价信息：")
print("=" * 50)
print(result)
print("=" * 50)
