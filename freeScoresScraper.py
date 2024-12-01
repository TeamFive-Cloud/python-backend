import requests
from bs4 import BeautifulSoup
import json
import time
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class FreeScoresScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        self.scores_data = []

    def fetch_page(self, url, retries=3):
        """获取网页内容"""
        print(f"Fetching page: {url}")
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = response.apparent_encoding
                print(f"Response status code: {response.status_code}")
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"获取页面失败: {response.status_code}")
                    return None
            except Exception as e:
                print(f"请求发生错误: {str(e)}")
                if attempt < retries - 1:
                    print("重试中...")
                    time.sleep(2)
                else:
                    return None

    def parse_free_scores(self, html_content):
        """解析 free-scores.com 乐谱信息"""
        soup = BeautifulSoup(html_content, 'html.parser')
        score_items = soup.select('div.flex-item_public_listing')  # 根据实际的HTML结构调整选择器
        
        for item in score_items:
            try:
                title_tag = item.select_one('a.g b')
                title = title_tag.get_text().strip() if title_tag else 'N/A'
                detail_page_tag = item.select_one('a[href*="download-sheet-music.php?pdf="]')
                detail_page_url = "https:" + detail_page_tag['href'] if detail_page_tag else None
                
                if detail_page_url:
                    detail_page_content = self.fetch_page(detail_page_url)
                    if detail_page_content:
                        self.parse_free_scores_detail(detail_page_content, title, detail_page_url)
                else:
                    print(f"未找到详细页面链接: {title}")
            except Exception as e:
                print(f"解析乐谱出错: {str(e)}")
                continue

    def parse_free_scores_detail(self, html_content, title, detail_page_url):
        """解析 free-scores.com 乐谱详细信息"""
        soup = BeautifulSoup(html_content, 'html.parser')
        pdf_link_tag = soup.select_one('a[href*=".pdf"]')
        pdf_link = pdf_link_tag['href'] if pdf_link_tag else 'N/A'
        mp3_link_tag = soup.select_one('a[href*=".mp3"]')
        mp3_link = "https:" + mp3_link_tag['href'] if mp3_link_tag else 'N/A'
        
        self.scores_data.append({
            'title': title,
            'detail_page_url': detail_page_url,
            'pdf_link': pdf_link,
            'mp3_link': mp3_link
        })
        print(f"成功解析乐谱详细信息: {title}")

    def crawl(self):
        """爬取 free-scores.com 网站的乐谱信息"""
        url = 'https://www.free-scores.com/free-sheet-music.php'
        html_content = self.fetch_page(url)
        
        if html_content:
            self.parse_free_scores(html_content)
        
        # 添加随机延迟
        time.sleep(random.uniform(2, 4))

def main():
    scraper = FreeScoresScraper()
    scraper.crawl()

    # 将所有乐谱信息保存到一个文件中
    if scraper.scores_data:
        with open('freeScores.json', 'w', encoding='utf8') as f:
            json.dump(scraper.scores_data, f, ensure_ascii=False, indent=4)
        print(f"所有乐谱数据已保存到 freeScores.json")
    else:
        print("没有数据可保存")

if __name__ == "__main__":
    main()