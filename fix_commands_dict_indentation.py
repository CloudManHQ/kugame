#!/usr/bin/env python3
"""
修复kubernetes_commands.py中commands字典的整体缩进错误
"""

def fix_commands_dict_indentation(file_path):
    """修复commands字典的整体缩进"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_commands_dict = False
    
    for line in lines:
        # 检查是否进入commands字典
        if 'commands: Dict[str, Any] = {' in line:
            in_commands_dict = True
            fixed_lines.append(line)
        # 检查是否退出commands字典
        elif 'return commands' in line and in_commands_dict:
            in_commands_dict = False
            fixed_lines.append(line)
        elif in_commands_dict:
            # 为字典内的所有行增加4个空格的缩进
            fixed_line = ' ' * 4 + line
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("commands字典整体缩进已修复")

if __name__ == "__main__":
    file_path = "kugame/kubernetes_commands.py"
    fix_commands_dict_indentation(file_path)
