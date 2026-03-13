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

def make_run_agent(agent):
    def run_agent(query: str) -> str:
        result_dict = agent.invoke({"messages": [HumanMessage(content=query)]})
        return result_dict["messages"][-1].content
    return run_agent
class AISkillService:
    """AI技能服务封装类，对外提供完整的技能匹配、脚本执行、文档参考能力"""

    def __init__(self, skill_root_dir: str = "./skills"):
        """
        初始化服务
        :param skill_root_dir: 技能文件夹根路径，默认./skills
        """
        self.skill_root_dir = skill_root_dir
        self.skill_schema = self.get_skill_schema()  # 预加载所有技能schema
        #self.skill_schema_str = " ".join(self.skill_schema)

    def get_content_between_separators(self, file_path: str) -> str:
        """
        提取文件中--- ---之间的内容并转为JSON字符串
        :param file_path: SKILL.md文件的路径
        :return: 格式化后的JSON字符串（键值对形式）
        """
        in_content = False
        target_content = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()
                    if stripped_line == '---' and not in_content:
                        in_content = True
                        continue
                    elif stripped_line == '---' and in_content:
                        in_content = False
                        break
                    if in_content and stripped_line:
                        target_content.append(stripped_line)
        except FileNotFoundError:
            print(f"警告：文件 {file_path} 不存在")
            return json.dumps({}, ensure_ascii=False)
        except Exception as e:
            print(f"读取文件 {file_path} 异常：{e}")
            return json.dumps({}, ensure_ascii=False)

        result = {}
        for line in target_content:
            if ":" not in line:
                continue  # 跳过无效键值对
            k, v = line.split(":", 1)  # 按第一个冒号分割，避免值中包含冒号
            result[k.strip()] = v.strip()
        with open(file_path, 'r', encoding='utf-8') as f:
            content=f.read().strip()
        folder_path = os.path.dirname(file_path)
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        result["all_description"]=content+f"当前时间是{formatted},文件路径是{folder_path}"
        return json.dumps(result, ensure_ascii=False)

    def get_first_level_subdirs(self) -> list:
        """
        获取技能根目录下的所有一级子目录对应的SKILL.md路径
        :return: SKILL.md文件路径列表
        """
        if not os.path.exists(self.skill_root_dir):
            print(f"警告：技能根目录 {self.skill_root_dir} 不存在")
            return []

        all_items = os.listdir(self.skill_root_dir)
        first_level_subdirs = [
            item for item in all_items
            if os.path.isdir(os.path.join(self.skill_root_dir, item))
        ]

        skill_file_paths = [
            os.path.join(self.skill_root_dir, subdir, "SKILL.md")
            for subdir in first_level_subdirs
        ]
        return skill_file_paths

    def get_skill_schema(self) -> list:
        """
        获取所有技能的schema信息
        :return: 各技能schema的列表
        """
        skill_files = self.get_first_level_subdirs()
        results = []
        for f in skill_files:
            content = self.get_content_between_separators(f)
            results.append(eval(content))
        return results
 

    def process_query(self, query: str) -> str:
        """
        处理用户查询的核心流程（对外核心接口）
        :param query: 用户输入查询内容
        :return: 最终处理结果字符串
        """
 
        skill_agents = []
        from langchain_core.tools import StructuredTool
        #构建各个子智能体
        for skill in self.skill_schema:
            name=skill["name"]
            #完整加载提示词
            agent=create_agent(llm,system_prompt=skill["all_description"],tools=[read_file,write_file,create_directory,execute_code])

            #只加载部分提示词
            tool = StructuredTool.from_function(
                func=make_run_agent(agent),  
                name=name,
                description=skill["description"]
            )
            skill_agents.append(tool)
        router_prompt = "你是一个主控智能体，可以根据用户的问题，选择合适的工具（技能）来完成任务。当你决定调用某个工具时，必须直接将用户的原始问题作为该工具的唯一参数，不要添加任何额外说明或改写。"
        router_agent = create_agent(
            llm,
            tools=skill_agents,  # 把工具列表传给它
            system_prompt=router_prompt
        )
        #result=router_agent.invoke({"messages": HumanMessage(content=query)})
        for s in router_agent.stream({"messages": HumanMessage(content=query)}):
            print (s)
        # for s in agent.stream({"messages": HumanMessage(content=query)}):
        #     print (s)
        #return result