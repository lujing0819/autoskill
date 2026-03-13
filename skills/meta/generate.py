from qwen_config import llm_coder
import sys
query = sys.argv[1]
save_path = sys.argv[2]
print ("代码生成器接收到的参数：", sys.argv)  # 打印接收到的参数，便于调试
prompt="  请根据上述需求生成一段可直接运行的纯Python代码，不要任何解释文字，不要```python，不要'''，不要markdown格式，不要多余注释，只输出干净的代码。"
response = llm_coder.invoke(query+prompt).content
with open(save_path, "w", encoding="utf-8") as f:
    f.write(response)