#!/usr/bin/env python3
"""
修复kubernetes_commands.py中注释行的缩进错误
"""

def fix_comment_indentation(file_path):
    """修复文件中注释行的缩进错误"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    in_dict_section = False

    for line in lines:
        # 检查是否在commands字典内部
        if 'def _initialize_commands' in line:
            in_dict_section = True
        elif 'return commands' in line and in_dict_section:
            in_dict_section = False

        if in_dict_section:
            stripped = line.lstrip()
            if stripped.startswith('#'):  # 注释行
                # 确保注释与字典键对齐（8个空格）
                fixed_line = ' ' * 8 + stripped
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print("注释缩进错误已修复")

if __name__ == "__main__":
    file_path = "kugame/kubernetes_commands.py"
    fix_comment_indentation(file_path)
