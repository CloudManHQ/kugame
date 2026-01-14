# 批量修复辅助脚本文件中的代码质量问题
import os

# 需要修复的文件列表
auxiliary_scripts = [
    'fix_blank_lines.py',
    'fix_commands_dict_indentation.py',
    'fix_comment_indentation.py',
    'fix_duplicate_keys.py',
    'fix_extra_commas.py',
    'fix_final_indentation_issues.py',
    'fix_indentation.py',
    'fix_only_commands_dict.py',
    'fix_trailing_whitespace.py',
    'fix_whitespace.py',
    'fix_syntax.py',
    'fix_encoding.py'
]

def fix_file(file_path: str) -> None:
    """修复单个文件的代码质量问题"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 修复行尾空格和空行包含空格
        fixed_lines = []
        for line in lines:
            if line.strip() == '':
                # 空行应该完全为空
                fixed_lines.append('\n')
            else:
                # 移除行尾空格
                fixed_lines.append(line.rstrip() + '\n')
        
        # 确保文件末尾有一个换行符
        if fixed_lines and not fixed_lines[-1].endswith('\n'):
            fixed_lines[-1] += '\n'
        
        # 修复特定文件的已知问题
        if file_path == 'fix_duplicate_keys.py':
            # 移除未使用的导入
            fixed_lines = [line for line in fixed_lines 
                         if not line.strip().startswith('from typing import Dict, Any')]
            fixed_lines = [line.replace('from typing import Dict, Any', '') for line in fixed_lines]
        
        if file_path == 'fix_indentation.py':
            # 移除未使用的re导入
            fixed_lines = [line for line in fixed_lines if not line.strip().startswith('import re')]
        
        if file_path in ['fix_final_indentation_issues.py', 'fix_only_commands_dict.py']:
            # 修复二进制运算符后的换行问题
            for i, line in enumerate(fixed_lines):
                if '==' in line and line.strip().endswith('=='):
                    fixed_lines[i] = line.rstrip() + ' '  # 确保运算符后有空格
        
        # 写入修复后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print(f"修复完成: {file_path}")
        
    except Exception as e:
        print(f"修复文件 {file_path} 时出错: {e}")

# 修复所有辅助脚本文件
for script in auxiliary_scripts:
    if os.path.exists(script):
        fix_file(script)
    else:
        print(f"跳过不存在的文件: {script}")

print("\n所有辅助脚本文件修复完成！")
