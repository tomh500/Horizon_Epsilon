import os

def convert_to_lf(file_path):
    with open(file_path, 'rb') as f:
        content = f.read().replace(b'\r\n', b'\n')  # 替换 CRLF 为 LF

    with open(file_path, 'wb') as f:
        f.write(content)

# 遍历当前目录及子目录
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".cfg"):
            convert_to_lf(os.path.join(root, file))
