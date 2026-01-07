#!/usr/bin/env python3
"""修复 kubernetes_commands.py 中的重复字典键"""

import re
import sys
from typing import Dict, Any


def fix_duplicate_keys(file_path: str) -> None:
    """修复文件中的重复字典键
    
    Args:
        file_path: 文件路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 先找到方法定义
        method_start = content.find('def _initialize_commands')
        if method_start == -1:
            print("未找到_initialize_commands方法")
            return
        
        # 找到方法中的 return {
        dict_start = content.find('return {', method_start)
        if dict_start == -1:
            print("未找到字典开始")
            return
        
        # 找到对应的结束大括号
        open_braces = 1
        dict_end = dict_start + 8  # 跳过 "return {"
        
        while dict_end < len(content) and open_braces > 0:
            if content[dict_end] == '{':
                open_braces += 1
            elif content[dict_end] == '}':
                open_braces -= 1
            dict_end += 1
        
        if open_braces != 0:
            print("未找到匹配的结束大括号")
            return
        
        # 提取字典内容
        dict_content = content[dict_start:dict_end]
        
        # 修复重复键
        fixed_dict = remove_duplicate_keys(dict_content)
        
        # 替换原始字典内容
        new_content = content[:dict_start] + fixed_dict + content[dict_end:]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("重复键修复完成")
        
    except Exception as e:
        print(f"修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


def remove_duplicate_keys(dict_content: str) -> str:
    """从字典内容中移除重复键
    
    Args:
        dict_content: 字典内容字符串
    
    Returns:
        修复后的字典内容
    """
    # 使用正则表达式匹配字典键值对
    key_pattern = r'"([^"]+)"\s*:\s*KubectlCommand'
    keys = re.findall(key_pattern, dict_content)
    
    # 找出重复的键
    key_counts = {}
    duplicate_keys = set()
    
    for key in keys:
        key_counts[key] = key_counts.get(key, 0) + 1
        if key_counts[key] > 1:
            duplicate_keys.add(key)
    
    print(f"发现重复键: {duplicate_keys}")
    
    if not duplicate_keys:
        return dict_content
    
    # 移除重复键（保留第一个出现的）
    fixed_content = dict_content
    
    for key in duplicate_keys:
        # 匹配第一个出现的键值对
        first_occurrence = re.search(rf'"{key}"\s*:\s*KubectlCommand\(.*?\)', fixed_content, re.DOTALL)
        if first_occurrence:
            # 移除后续所有出现的键值对
            remaining_content = fixed_content[first_occurrence.end():]
            # 匹配后续的所有相同键值对
            subsequent_pattern = rf'\s*"{key}"\s*:\s*KubectlCommand\(.*?\)'
            # 替换后续所有出现的键值对为空白
            cleaned_remaining = re.sub(subsequent_pattern, '', remaining_content, flags=re.DOTALL)
            # 重新组合内容
            fixed_content = fixed_content[:first_occurrence.end()] + cleaned_remaining
    
    return fixed_content


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python fix_duplicate_keys.py <file_path>")
        sys.exit(1)
    
    fix_duplicate_keys(sys.argv[1])