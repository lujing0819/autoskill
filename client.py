from AI_Service import AISkillService
# ------------------- 本地调用示例（对外提供的简单接口） -------------------
# 2. 加载用户查询（支持从文件/直接传入字符串）
# 方式A：从文件加载查询
def load_query_from_file(file_path: str) -> str:
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"读取查询文件异常：{e}")
        return ""
if __name__ == "__main__":
    # 1. 实例化技能服务（可指定自定义技能根目录）
    ai_skill_service = AISkillService(skill_root_dir="./skills")
    # 3. 处理查询（核心对外接口）
    #query="我要生成一个Python脚本，计算两个数相乘，"
    query="123123*343245是多少？"
    result = ai_skill_service.process_query(query)

    # 4. 输出结果
    print("\n==================== 最终服务结果 ====================")
    print(result)