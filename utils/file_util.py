def replace(file, old_content, new_content):
    # 传入文件(file),将旧内容(old_content)替换为新内容(new_content)
    content = read_file(file)
    content = content.replace(old_content, new_content)
    rewrite_file(file, content)


def read_file(file):
    # 读文件内容
    with open(file, encoding='UTF-8') as f:
        read_all = f.read()
        f.close()

    return read_all


def rewrite_file(file, data):
    # 写内容到文件
    with open(file, 'w', encoding='UTF-8') as f:
        f.write(data)
        f.close()
