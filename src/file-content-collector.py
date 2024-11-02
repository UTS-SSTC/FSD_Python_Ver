import os
import sys


def collect_files_content(output_file='collected_contents.txt', encoding='utf-8'):
    """
    收集当前目录下所有文件的路径和内容,按指定格式保存到输出文件中
    格式:
    <相对路径>
    <内容>
    
    Args:
        output_file (str): 输出文件名
        encoding (str): 文件编码,默认utf-8
    """

    def is_binary_file(file_path):
        """
        检查文件是否是二进制文件
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
                return False
        except UnicodeDecodeError:
            return True

    def write_file_content(file_path, out_file):
        """
        将单个文件的路径和内容写入输出文件
        """
        rel_path = os.path.relpath(file_path)

        # 跳过输出文件本身
        if rel_path == output_file:
            return

        out_file.write(f"<{rel_path}>\n")

        # 检查是否为二进制文件
        if is_binary_file(file_path):
            out_file.write("[二进制文件,内容已忽略]\n")
        else:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    out_file.write(f"{content}\n")
            except Exception as e:
                out_file.write(f"[读取文件失败: {str(e)}]\n")

        out_file.write("\n")  # 在每个文件记录之间添加空行

    # 获取所有文件路径并排序，确保输出顺序一致
    all_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file != output_file:  # 排除输出文件
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    all_files.sort()  # 对文件路径进行排序

    # 写入所有文件内容
    with open(output_file, 'w', encoding=encoding) as out_file:
        for file_path in all_files:
            write_file_content(file_path, out_file)


if __name__ == "__main__":
    try:
        # 可以通过命令行参数指定输出文件名和编码
        output_file = sys.argv[1] if len(sys.argv) > 1 else 'collected_contents.txt'
        encoding = sys.argv[2] if len(sys.argv) > 2 else 'utf-8'

        collect_files_content(output_file, encoding)
        print(f"文件内容已收集到: {output_file}")

    except Exception as e:
        print(f"错误: {str(e)}")
