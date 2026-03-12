import sys
from io import StringIO
from utils import execute_code
def call_llm(prompt):
    # 模拟 LLM 返回代码
    return """
import math
radius = 5
area = math.pi * radius ** 2
result = round(area, 2)
"""

 

# 主程序
prompt = "写一个计算圆面积的代码"
code = call_llm(prompt)
print("生成的代码：\n", code)

result, output, error = execute_code(code, 'result')
if error:
    print("执行错误:", error)
else:
    print("执行结果（变量 result）:", result)
    print("程序输出:\n", output)