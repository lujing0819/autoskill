#!/usr/bin/env python3
"""
平安银行股价查询脚本
"""
import sys
import os

# 添加技能路径
sys.path.insert(0, '/skills/stockprice')

from query import query

# 执行查询
user_query = "平安银行最近20天的股价"
result = query(user_query)

# 输出结果
print("=" * 60)
print(f"查询: {user_query}")
print("=" * 60)
print(result)
print("=" * 60)

# 保存结果到文件
with open('/workspace/stockprice_result.txt', 'w', encoding='utf-8') as f:
    f.write(result)

print("结果已保存到 /workspace/stockprice_result.txt")
