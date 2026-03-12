import sys
sys.path.insert(0, '/skills/stockprice')

from query import query

# 调用 query 函数查询平安银行最近20天股价
result = query("平安银行最近20天股价")
print(result)
