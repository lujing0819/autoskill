import sys
sys.path.insert(0, '/skills/stockprice')
from query import query
result = query("平安银行最近20天股价")
with open('/workspace/final_result.txt', 'w', encoding='utf-8') as f:
    f.write(result)
