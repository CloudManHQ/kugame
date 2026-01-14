# 修复story.py文件中的行尾空格
with open('./kugame/story.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 修复所有行尾空格
fixed_lines = []
for line in lines:
    # 删除行尾空格并添加正确的换行符
    fixed_line = line.rstrip() + '\n'
    fixed_lines.append(fixed_line)

# 确保文件末尾有一个换行符
if fixed_lines and not fixed_lines[-1].endswith('\n'):
    fixed_lines[-1] += '\n'

with open('./kugame/story.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print('行尾空格修复完成！')
