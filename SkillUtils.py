from qwen_config import llm_large
from utils import get_code
from langchain_core.tools import tool
import sys
import sys
from io import StringIO
import json
import os
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
def execute_code(code_str, result_var='result'):
    """
    在隔离的命名空间中执行给定的 Python 代码字符串，并捕获执行结果、标准输出和错误信息。
    此函数专为智能体调用设计，允许动态运行代码片段并获取其输出和返回值。

    参数
    ----------
    code_str : str
        要执行的 Python 代码字符串。代码将在空的命名空间中运行，无法访问外部变量。
    result_var : str, 可选
        代码执行后需要从命名空间中提取的变量名（默认为 'result'）。
        执行后，函数会尝试从命名空间中获取该变量的值作为主要返回结果。

    返回值
    -------
    tuple
        (result, output, error) 包含三个元素：
        - result : any
            从命名空间中获取的 result_var 变量的值。如果变量不存在或代码执行出错，则为 None。
        - output : str
            代码执行期间捕获的标准输出（通过 print 等打印的内容）。
        - error : str 或 None
            如果执行过程中发生异常，返回异常信息的字符串表示；否则为 None。

    注意事项
    --------
    - 由于 exec 在空的命名空间中执行，代码中定义的变量（包括 result_var）都位于该局部命名空间内。
    - 此函数会临时替换 sys.stdout 以捕获输出，因此不会影响外部环境的输出。
    - **安全警告**：exec 可以执行任意代码，请确保 code_str 来源可信，避免执行恶意或不受信任的代码。
    - 如果代码语法错误或运行时异常，error 将包含异常信息，此时 result 为 None。
 
    """
    # 准备命名空间
    namespace = {}
    # 捕获输出
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    error = None
    try:
        exec(code_str, namespace)
    except Exception as e:
        error = str(e)
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    result = namespace.get(result_var)
    return result, output, error