import requests
from bs4 import BeautifulSoup
import os


def get_novel_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf - 8'
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', id='nr')
        if content_div:
            text_parts = []
            for element in content_div.stripped_strings:
                text_parts.append(element)
            content = '\n'.join(text_parts)
            return content
        else:
            print("未找到正文所在的 div 标签。")
            return None
    except requests.RequestException as e:
        print(f"请求网页时出现错误: {e}")
        return None


def get_next_chapter_url(soup):
    next_link = soup.find('a', id='pt_next')
    if next_link:
        return next_link.get('href')
    return None


def save_novel_to_md(novel_content, save_path):
    try:
        with open(save_path, 'w', encoding='utf - 8') as md_file:
            md_file.write(novel_content)
        print(f"文件已成功保存到: {os.path.abspath(save_path)}，小说内容爬取与保存任务完成。")
    except Exception as e:
        print(f"保存文件时出现错误: {e}")


if __name__ == "__main__":
    start_url = "https://m.ltxs520.net/html/78/78509/5808917.html"
    base_url = "https://m.ltxs520.net"
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")

    save_dir = 'output'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, 'novel_content.md')
    all_novel_content = ""
    current_url = start_url
    chapter_num = 1
    while current_url:
        print(f"开始爬取第{chapter_num}章内容...")
        content = get_novel_content(current_url)
        if content:
            all_novel_content += content + '\n\n'
            response = requests.get(current_url)
            response.encoding = 'utf - 8'
            soup = BeautifulSoup(response.text, 'html.parser')
            next_chapter_url = get_next_chapter_url(soup)
            if next_chapter_url:
                current_url = base_url + next_chapter_url
            else:
                current_url = None
            chapter_num += 1
        else:
            current_url = None
    if all_novel_content:
        save_novel_to_md(all_novel_content, file_path)
    else:
        print("未获取到有效正文内容，文件未保存。")
