#!/usr/bin/env python3
"""
精确修复kubernetes_commands.py中_initialize_commands方法内commands字典的缩进错误
"""

def fix_only_commands_dict(file_path):
    """只修复_initialize_commands方法内commands字典的缩进"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_initialize_method = False
    in_commands_dict = False
    
    for line in lines:
        # 检查是否进入_initialize_commands方法
        if 'def _initialize_commands' in line:
            in_initialize_method = True
            fixed_lines.append(line)
        # 检查是否退出_initialize_commands方法
        elif 'return commands' in line and in_initialize_method:
            in_initialize_method = False
            in_commands_dict = False
            fixed_lines.append(line)
        elif in_initialize_method:
            # 检查是否进入commands字典
            if 'commands: Dict[str, Any] = {' in line:
                in_commands_dict = True
                fixed_lines.append(line)
            elif in_commands_dict:
                # 只处理commands字典内的内容
                stripped = line.lstrip()
                if not stripped:  # 空行
                    fixed_lines.append('\n')
                    continue
                
                # 命令定义行（字典键）
                if (':' in stripped and 
                    ('KubectlCommand' in stripped or 
                     'GenericCommand' in stripped or 
                     'CloudVendorCommand' in stripped)):
                    fixed_line = '            ' + stripped  # 12个空格
                    fixed_lines.append(fixed_line)
                
                # 注释行
                elif stripped.startswith('#'):
                    fixed_line = '            ' + stripped  # 12个空格
                    fixed_lines.append(fixed_line)
                
                # 命令内部参数行
                elif stripped.startswith(('name=', 'category=', 'description=', 'syntax=', 'example=', 'tool=', 'vendor=', 'service=', 'kubernetes_concept=', 'related_commands=', 'difficulty=')):
                    fixed_line = '                ' + stripped  # 16个空格
                    fixed_lines.append(fixed_line)
                
                # 命令结束括号行
                elif stripped.startswith('),'):
                    fixed_line = '            ' + stripped  # 12个空格
                    fixed_lines.append(fixed_line)
                
                # 字典结束括号行
                elif stripped.startswith('}'):
                    fixed_line = '        ' + stripped  # 8个空格（与return commands对齐）
                    fixed_lines.append(fixed_line)
                
                # 其他行在commands字典内保持不变
                else:
                    fixed_lines.append(line)
            else:
                # _initialize_commands方法内但不在commands字典内的行保持不变
                fixed_lines.append(line)
        else:
            # 文件其他部分的行保持不变
            fixed_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("已精确修复_initialize_commands方法内commands字典的缩进")

if __name__ == "__main__":
    file_path = "kugame/kubernetes_commands.py"
    fix_only_commands_dict(file_path)
