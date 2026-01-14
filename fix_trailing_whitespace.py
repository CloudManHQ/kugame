#!/usr/bin/env python3
"""修复尾随空格问题"""

import sys


def fix_trailing_whitespace(file_path: str) -> None:
    """修复文件中的尾随空格

    Args:
        file_path: 文件路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed_lines = []
        for line in lines:
            # 移除行末的尾随空格
            fixed_line = line.rstrip() + '\n'
            fixed_lines.append(fixed_line)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)

        print("尾随空格修复完成")

    except Exception as e:
        print(f"修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python fix_trailing_whitespace.py <file_path>")
        sys.exit(1)

    fix_trailing_whitespace(sys.argv[1])
