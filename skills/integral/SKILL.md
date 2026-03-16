---
name: integral
description:你是一个专业的工具生成器，当任务需要使用工具时，你会根据智能体的需求生成相应的工具。 
---
技能使用具体方法
调用工具脚本通过
python -m skills.integral.compute query arg1 arg2 arg3
arg1 arg2 arg3为脚本需要的数组  包括被积函数表达式、积分下限、积分上限以及结果保存路径，然后通过读取结果文件，获取工具执行结果。
