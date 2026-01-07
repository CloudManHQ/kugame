#!/usr/bin/env python3
"""修复空白行中的空格问题"""

import sys


def fix_blank_lines(file_path: str) -> None:
    """修复文件中的空白行空格问题
    
    Args:
        file_path: 文件路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        for line in lines:
            # 如果是空白行但包含空格，将其转换为真正的空白行
            if line.strip() == '' and line != '\n':
                fixed_lines.append('\n')
            else:
                fixed_lines.append(line)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("空白行空格修复完成")
        
    except Exception as e:
        print(f"修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python fix_blank_lines.py <file_path>")
        sys.exit(1)
    
    fix_blank_lines(sys.argv[1])