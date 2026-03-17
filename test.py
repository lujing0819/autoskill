import os
import json
import re
# 注意：保留原有依赖导入，若llm_config不存在，可预留接口
from qwen_config import llm
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage,AIMessage,ToolMessage
from SkillUtils import read_file,write_file,create_directory,execute_code
from langchain.agents import create_agent 
from datetime import datetime
import os
import ast
import importlib.util
import sys
from langchain_core.tools import Tool

agent=create_agent(llm,system_prompt=skill["all_description"],tools=tools)
for s in agent.stream({"messages": HumanMessage(content=query)}):
    print (s)
