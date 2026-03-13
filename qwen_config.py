'''
qwen_llm 的 Docstring
调用百炼平台的qwen
'''
 
from langchain_openai import ChatOpenAI
import os
llm_coder = ChatOpenAI(
    model="qwen3-coder-plus",
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    api_key=os.getenv("api_key")
)
llm_large = ChatOpenAI(
    model="qwen3.5-plus",
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    api_key=os.getenv("api_key")
)
llm=llm_large