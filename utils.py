import sys
from io import StringIO
import json

import re
def get_code(text: str) -> str:
    # 尝试匹配 Markdown 代码块（如果有）
    code_block_pattern = r"```(?:python)?\s*\n(.*?)```"
    matches = re.findall(code_block_pattern, text, re.DOTALL)
    if matches:
        # 返回第一个代码块的内容，并去除首尾空白
        return matches[0].strip()
    
    # 如果没有代码块，就认为整个文本就是代码（去除可能的解释性头尾）
    # 简单处理：假设代码是连续的，可以按行过滤掉空行或注释行（可选）
    return text.strip()