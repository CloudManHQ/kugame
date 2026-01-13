# 修复story.py文件中的编码问题
with open('./kugame/story.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 修复所有乱码字符
content = content.replace('\ufffd', '')

# 修复ASCII图像中的乱码边框
content = content.replace('?', '')

# 修复未终止的三引号字符串
if content.count('"""') % 2 != 0:
    # 在文件末尾添加三引号关闭字符串
    content += '"""'

with open('./kugame/story.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('修复完成！')
