#!/usr/bin/env python3
"""
修复kubernetes_commands.py中的缩进错误
"""

def fix_indentation(file_path):
    """修复文件中的缩进错误"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    in_dict_section = False

    current_indent = 0
    in_dict_section = False

    for line in lines:
        # 检查是否在commands字典内部
        if 'def _initialize_commands' in line:
            in_dict_section = True
        elif 'return commands' in line and in_dict_section:
            in_dict_section = False

        if in_dict_section:
            # 检测当前行的缩进级别
            stripped = line.lstrip()
            if not stripped:  # 空行
                fixed_lines.append(line)
                continue

            indent_level = len(line) - len(stripped)

            # 字典键行（如 "kubectl run": KubectlCommand(）
            if ':' in stripped and ('KubectlCommand' in stripped or 'GenericCommand' in stripped or 'CloudVendorCommand' in stripped):
                # 确保字典键行有8个空格缩进
                fixed_line = ' ' * 8 + stripped
                current_indent = 12  # 内部参数应该有12个空格缩进

            # 内部参数行
            elif stripped.startswith(('name=', 'category=', 'description=', 'syntax=', 'example=', 'tool=', 'vendor=', 'service=', 'kubernetes_concept=', 'related_commands=', 'difficulty=')):
                # 确保内部参数有12个空格缩进
                fixed_line = ' ' * 12 + stripped

            # 结束括号行
            elif stripped.startswith('),') or stripped.startswith('}'):
                # 确保结束括号与字典键对齐（8个空格）
                fixed_line = ' ' * 8 + stripped

            # 注释行
            elif stripped.startswith('#'):
                # 确保注释与上下文对齐
                if indent_level < 8:
                    fixed_line = ' ' * 8 + stripped
                else:
                    fixed_line = line

            else:
                fixed_line = line

            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print("缩进错误已修复")

if __name__ == "__main__":
    file_path = "kugame/kubernetes_commands.py"
    fix_indentation(file_path)
