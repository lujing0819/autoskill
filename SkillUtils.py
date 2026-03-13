from qwen_config import llm_large
from utils import get_code
from langchain_core.tools import tool
import sys
import sys
from io import StringIO
import json
import os
import subprocess
import shlex
import sys
@tool
def create_directory(path):
    """
    创建指定路径的文件夹（包括所有必需的父目录）。

    此函数旨在作为 LangGraph 智能体中的工具，用于创建目录。
    如果目录已存在，不会报错（类似 mkdir -p），并视为操作成功。

    参数:
        path (str): 需要创建的文件夹路径。

    返回:
        str: 操作结果描述。成功时返回 "成功创建文件夹：/path"；
             如果发生异常（如路径已存在但不是目录、权限不足等），返回错误信息字符串。
    """
    print (f"正在创建目录：{path}")
    try:
        os.makedirs(path, exist_ok=True)
        return f"成功创建文件夹：{path}"
    except Exception as e:
        return f"创建失败：{str(e)}"
@tool
def read_file(path):
    """
    读取文件内容并返回去除首尾空白字符的字符串。

    此函数旨在作为 LangGraph 智能体中的工具，用于文件读取操作。

    参数:
        path (str): 需要读取的文件路径。

    返回:
        str: 去除首尾空白后的文件内容。
    """
    print (f"正在读取文件：{path}")
    with open(path,encoding="utf-8") as f:
        content = f.read().strip()
    return content

@tool
def write_file(path, content, mode='w', encoding='utf-8'):
    """
    将字符串内容写入指定文件，并返回操作结果信息。

    此函数旨在作为 LangGraph 智能体中的工具，用于文件写入操作。
    支持覆盖写入（默认）或追加写入，并自动处理编码。

    参数
    ----------
    path : str
        目标文件路径。
    content : str
        要写入文件的字符串内容。
    mode : str, 可选
        文件打开模式，默认为 'w'（覆盖写入）。可使用 'a' 进行追加写入。
        注意：二进制写入模式（如 'wb'）未在本函数中测试，建议仅使用文本模式。
    encoding : str, 可选
        文件编码，默认为 'utf-8'。

    返回
    -------
    str
        操作结果描述。成功时返回类似 "成功写入文件：/path/to/file" 的信息；
        如果发生异常，则返回错误信息字符串（例如 "写入失败：权限不足"）。

    异常
    --------
    本函数内部捕获所有异常并返回错误字符串，不会向外抛出异常。
    """
    print (f"正在写入文件：{path}，内容长度：{len(content)}，模式：{mode}")
    try:
        with open(path, mode, encoding=encoding) as f:
            f.write(content)
        return f"成功写入文件：{path}"
    except Exception as e:
        return f"写入失败：{str(e)}"
@tool
def generate_and_exe_code(content):
    """
    代码生成器

    该函数根据用户输入的需求描述（content），构造提示词并调用大模型生成可直接运行的 Python 代码。
    生成的代码必须将最终计算结果赋值给变量 `result`。函数会从模型响应中提取代码块，并返回可执行代码
     

    Args:
        content (str): 描述需要解决的问题或待处理的数据，用于指导 LLM 生成代码。
    Returns:
        any: 如果代码生成和执行成功，返回代码执行后 `result` 变量的值（具体类型由生成的代码决定）。
        str: 如果代码解析失败，返回字符串 "代码解析失败"。
    """
    print (f"正在生成代码，输入内容长度：{len(content)}")
    prompt=f"{content} 根据上述信息，生成可以直接执行的代码，请只输出纯文本代码，不要用 ``` 包裹。"
    # print (prompt)
    # result=llm_large.invoke(prompt).content
    # code=get_code(result)
    with open("code.py") as f:
        code=f.read()
    print (f"生成的代码长度：{len(code)}，内容预览...")
    return code

@tool
def generate_content(content):
    """
    内容生成器

    通用内容生成器

    该函数直接调用大模型进行文本生成，适用于问答、文本创作、总结等普通自然语言处理任务。
    将尽可能多的提示词，提示词来自于智能体的system_prompt，信息输入进来，确保生成返回结果符合预期
    返回大模型生成的原始文本回答，文本创作、总结等普通自然语言处理任务。

    Args:
        content (str): 输入内容
    Returns:
        any: 如果代码生成和执行成功，返回代码执行后 `result` 变量的值（具体类型由生成的代码决定）。
        str: 如果代码解析失败，返回字符串 "代码解析失败"。
    """
    result=llm_large.invoke(content).content
    return result

@tool
def execute_code(command, result_var='result'):
    """
    运行python脚本时，执行代码字符串并返回结果  
    在隔离环境中执行给定的命令行指令，并捕获执行结果、标准输出和错误信息。
    此函数专为智能体调用设计，允许动态运行命令行并获取输出与返回状态。

    参数
    ----------
    command : str
        要执行的命令行指令字符串，例如 "python test.py"、"ls"、"dir" 等。

    返回值
    -------
    tuple
        (returncode, output, error) 包含三个元素：
        - returncode : int
            命令执行后的返回码，0 表示成功，非 0 表示失败。
        - output : str
            命令执行期间捕获的标准输出（stdout）。
        - error : str
            命令执行期间捕获的标准错误（stderr）。

    注意事项
    --------
    - 命令将在独立的子进程中运行，不会污染当前程序环境。
    - 执行超时、命令不存在、权限不足等异常都会被捕获并返回错误信息。
    - **安全警告**：请勿执行来源不可信的命令，避免注入攻击或恶意操作。
    """
    #try:
    if True:
        # 安全解析字符串命令
        args = shlex.split(command)
        # 替换为当前环境的 python 路径，避免环境错误
        if args[0] == "python":
            args[0] = sys.executable
        print ("aaa",args)
        # 执行命令
        
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding="gbk",
        )

        return result.returncode, result.stdout.strip(), result.stderr.strip()

    # except Exception as e:
    #     return -1, "", f"执行异常：{str(e)}"