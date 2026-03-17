"""
定积分计算器模块

该模块提供计算定积分的功能，支持多种数学函数的积分计算。
"""

import sympy
from sympy import sympify, Symbol, integrate


def calculate_definite_integral(function_str: str, lower_limit: float, upper_limit: float) -> dict:
    """
    计算给定函数在指定区间上的定积分
    
    参数:
        function_str (str): 被积函数的字符串表达式，例如 "x**2", "sin(x)", "exp(x)" 等
        lower_limit (float): 积分下限
        upper_limit (float): 积分上限
    
    返回:
        dict: 包含计算结果的字典，格式为:
            {
                "success": bool,  # 是否计算成功
                "result": float or str,  # 计算结果（数值或符号表达式）
                "message": str  # 错误信息（如果失败）
            }
    
    示例:
        >>> calculate_definite_integral("x**2", 0, 1)
        {"success": True, "result": 0.3333333333333333, "message": ""}
        
        >>> calculate_definite_integral("sin(x)", 0, 3.14159)
        {"success": True, "result": 1.9999999999999998, "message": ""}
    """
    try:
        # 定义符号变量
        x = Symbol('x')
        
        # 将字符串表达式转换为sympy表达式
        function = sympify(function_str)
        
        # 计算定积分
        result = integrate(function, (x, lower_limit, upper_limit))
        
        # 尝试将结果转换为数值
        try:
            numerical_result = float(result.evalf())
            return {
                "success": True,
                "result": numerical_result,
                "message": ""
            }
        except (TypeError, ValueError):
            # 如果无法转换为数值，返回符号表达式
            return {
                "success": True,
                "result": str(result),
                "message": ""
            }
            
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "message": f"计算失败: {str(e)}"
        }


if __name__ == "__main__":
    # 测试示例
    test_cases = [
        ("x**2", 0, 1),
        ("sin(x)", 0, 3.14159),
        ("exp(x)", 0, 1),
        ("1/x", 1, 2),
        ("x**3 + 2*x", -1, 1)
    ]
    
    print("定积分计算器测试:")
    print("-" * 50)
    
    for func, lower, upper in test_cases:
        result = calculate_definite_integral(func, lower, upper)
        if result["success"]:
            print(f"∫({func})dx from {lower} to {upper} = {result['result']}")
        else:
            print(f"计算 ∫({func})dx from {lower} to {upper} 失败: {result['message']}")
