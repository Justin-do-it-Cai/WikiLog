import difflib
import os
import glob

wikilog_dir = 'wikilog'  # wikilog目录路径
res_file = 'res/res.txt'  # 结果文件路径

# 确保结果文件所在目录存在
os.makedirs(os.path.dirname(res_file), exist_ok=True)

with open(res_file, 'w', encoding='utf-8') as output_file:
    for i in range(1, 222):
        # 构建当前和下一文件的路径
        current_file = os.path.join(wikilog_dir, f"{i}_*.txt")
        next_file = os.path.join(wikilog_dir, f"{i+1}_*.txt")

        # 使用glob模块找到匹配的文件名
        current_files = glob.glob(current_file)
        next_files = glob.glob(next_file)

        if current_files and next_files:
            # 只取找到的第一个文件
            with open(current_files[0], 'r', encoding='utf-8') as f1, open(next_files[0], 'r', encoding='utf-8') as f2:
                f1_lines = f1.readlines()
                f2_lines = f2.readlines()

                # 获取两个文件的差异
                diff = list(difflib.unified_diff(f1_lines, f2_lines))

                # 筛选出增加和删除的行
                adds = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
                dels = [line for line in diff if line.startswith('-') and not line.startswith('---')]

                # 写入结果文件
                output_file.write(f"第{i}次修改：\n")
                if dels:
                    output_file.write("del:" + "".join(dels))
                if adds:
                    output_file.write("add:" + "".join(adds) + "\n")
                output_file.write("\n")

print("完成比较并将结果保存到res.txt文件中。")
