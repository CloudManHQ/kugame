#!/usr/bin/env python3
"""
修复kubernetes_commands.py中剩余的缩进和空白行问题
"""

def fix_final_indentation_issues(file_path):
    """修复剩余的缩进和空白行问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []

    for line in lines:
        # 修复空白行中的空格（W293）
        stripped = line.strip()
        if not stripped:
            fixed_lines.append('\n')
            continue

        # 修复命令定义行和注释行的缩进
        current_stripped = line.lstrip()
        current_indent = len(line) - len(current_stripped)

        # 处理命令定义行（字典键）
        if (':' in current_stripped and
            ('KubectlCommand' in current_stripped or
             'GenericCommand' in current_stripped or
             'CloudVendorCommand' in current_stripped)):
            # 命令定义行应该有12个空格的缩进
            fixed_line = ' ' * 12 + current_stripped
            fixed_lines.append(fixed_line)

        # 处理注释行
        elif current_stripped.startswith('#'):
            # 注释行应该有12个空格的缩进（与命令定义行对齐）
            fixed_line = ' ' * 12 + current_stripped
            fixed_lines.append(fixed_line)

        # 处理命令内部参数行
        elif current_stripped.startswith(('name=', 'category=', 'description=', 'syntax=', 'example=', 'tool=', 'vendor=', 'service=', 'kubernetes_concept=', 'related_commands=', 'difficulty=')):
            # 参数行应该有16个空格的缩进
            fixed_line = ' ' * 16 + current_stripped
            fixed_lines.append(fixed_line)

        # 处理命令结束括号行
        elif current_stripped.startswith('),'):
            # 结束括号应该有12个空格的缩进（与命令定义行对齐）
            fixed_line = ' ' * 12 + current_stripped
            fixed_lines.append(fixed_line)

        # 其他行保持不变
        else:
            fixed_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print("最终的缩进和空白行问题已修复")

if __name__ == "__main__":
    file_path = "kugame/kubernetes_commands.py"
    fix_final_indentation_issues(file_path)
