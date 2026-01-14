# 修复story.py中的语法错误
with open('./kugame/story.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到需要修复的位置（第450行开始的ASCII艺术）
start_line = 450
end_line = 500  # 假设ASCII艺术在第500行前结束

# 创建修复后的内容
fixed_lines = lines[:450]  # 保留前450行
fixed_lines.append('            ),\n')  # 添加缺失的括号和逗号

# 找到第二章开始的位置
chapter_2_start = None
for i in range(500, len(lines)):
    if 'Chapter.第一章' in lines[i]:
        chapter_2_start = i
        break

# 如果找到第二章开始的位置，添加后续内容
if chapter_2_start is not None:
    fixed_lines.extend(lines[chapter_2_start:])

# 写入修复后的内容
with open('./kugame/story.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print('语法错误修复完成！')
