#!/usr/bin/env python3
"""修复 kubernetes_commands.py 中的多余逗号"""

import re
import sys


def fix_extra_commas(file_path: str) -> None:
    """修复文件中的多余逗号

    Args:
        file_path: 文件路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 修复连续的逗号
        # 匹配两个或更多连续的逗号
        fixed_content = re.sub(r',{2,}', ',', content)

        # 修复字典中的多余逗号（在大括号前）
        fixed_content = re.sub(r',\s*}', '}', fixed_content)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        print("多余逗号修复完成")

    except Exception as e:
        print(f"修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python fix_extra_commas.py <file_path>")
        sys.exit(1)

    fix_extra_commas(sys.argv[1])
