import re
from collections import Counter

def count_words(input_file, output_file):
    """
    统计文本文件中每个单词的出现次数，并将结果写入输出文件
    
    参数:
        input_file (str): 输入文本文件路径
        output_file (str): 输出结果文件路径
    """
    try:
        # 读取输入文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 提取单词并转换为小写
        words = re.findall(r'\b\w+\b', text.lower())
        
        # 统计词频
        word_counts = Counter(words)
        
        # 按词频降序排列，相同词频按字母顺序
        sorted_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        
        # 写入结果文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for word, count in sorted_counts:
                f.write(f"{word}: {count}\n")
                
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    # 示例用法
    count_words("input.txt", "output.txt")