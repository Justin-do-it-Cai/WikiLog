import requests
from bs4 import BeautifulSoup
import re
import os


def save_diffs(url, filename):
    edit_times = 0
    dir = "wikilog"
    while url:
        edit_times += 1
        # 请求页面内容
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.get_text()

        # 使用正则表达式找到第一个日期
        date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', text)
        if not date_match:
            print("未找到日期。")
            return

        date = date_match.group(0)
        # 将日期格式转换为文件名安全格式
        safe_date = date.replace('年', '-').replace('月', '-').replace('日', '')
        file_path = os.path.join(dir, f"{edit_times}_{safe_date}.txt")

        # 找到“取自”之前的所有文本
        key_info_start = text.find('\n', text.find(date) + len(date)) + 1
        key_info_end = text.find('取自“https://zh.wikipedia.org', key_info_start)
        key_info = text[key_info_start:key_info_end].strip()

        # 将找到的日期和关键信息写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{key_info}\n")
        print(f"edit_times={edit_times} successfully download\n")
        # 查找“下一版本→”链接
        next_link = soup.find('a', text="下一修订→")
        if next_link:
            url = f"https://zh.wikipedia.org{next_link.get('href')}"
        else:
            print("finish!\n")
            url = None


# 开始的URL
start_url = "https://zh.wikipedia.org/w/index.php?title=%E8%B4%B9%E5%AD%9D%E9%80%9A&direction=prev&oldid=19012"
save_diffs(start_url, 'wiki_revisions.txt')
