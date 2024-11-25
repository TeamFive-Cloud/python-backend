import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class MusicNewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.news_data = []

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

    def parse_themusic(self, html_content):
        """解析themusic.com.au新闻"""
        soup = BeautifulSoup(html_content, 'html.parser')
        news_items = soup.select('a[href^="/news/"]')  # 根据实际的HTML结构调整选择器
        
        for item in news_items:
            try:
                title = item.select_one('h2').get_text().strip() if item.select_one('h2') else 'N/A'
                description = item.select_one('p').get_text().strip() if item.select_one('p') else 'N/A'
                img_tag = item.select_one('img')
                img_url = img_tag['src'] if img_tag else 'N/A'
                link = "https://themusic.com.au" + item['href']
                
                self.news_data.append({
                    'source': 'The Music',
                    'title': title,
                    'description': description,
                    'img_url': img_url,
                    'link': link
                })
            except Exception as e:
                print(f"解析The Music新闻出错: {str(e)}")
                continue

    def crawl(self):
        """爬取themusic.com.au网站的新闻"""
        url = 'https://themusic.com.au/news?page=1'
        html_content = self.fetch_page(url)
        
        if html_content:
            self.parse_themusic(html_content)
        
        # 添加随机延迟
        time.sleep(random.uniform(2, 4))

class BillboardNewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.news_data = []

    def fetch_page(self, url, retries=3):
        """获取网页内容"""
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = response.apparent_encoding
                if response.status_code == 200:
                    print(f"成功获取页面: {url}")
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

    def parse_billboard(self, html_content):
        """解析billboard.com新闻"""
        soup = BeautifulSoup(html_content, 'html.parser')
        news_items = soup.select('.story .a-story-grid')  # 根据实际的HTML结构调整选择器
        
        if not news_items:
            print("未找到新闻项目")
        
        for item in news_items:
            try:
                title_tag = item.select_one('h3#title-of-a-story a.c-title__link')
                title = title_tag.get_text().strip() if title_tag else 'N/A'
                link = title_tag['href'] if title_tag else 'N/A'
                description = title  # 使用标题作为描述
                img_tag = item.select_one('img.c-lazy-image__img')
                img_url = img_tag['src'] if img_tag else 'N/A'
                
                self.news_data.append({
                    'source': 'Billboard',
                    'title': title,
                    'description': description,
                    'img_url': img_url,
                    'link': link
                })
                print(f"成功解析新闻: {title}")
            except Exception as e:
                print(f"解析Billboard新闻出错: {str(e)}")
                continue

    def crawl(self):
        """爬取billboard.com网站的新闻"""
        url = 'https://www.billboard.com/news'
        html_content = self.fetch_page(url)
        
        if html_content:
            self.parse_billboard(html_content)
        
        # 添加随机延迟
        time.sleep(random.uniform(2, 4))

def main():
    all_news = []

    music_scraper = MusicNewsScraper()
    music_scraper.crawl()
    all_news.extend(music_scraper.news_data)

    billboard_scraper = BillboardNewsScraper()
    billboard_scraper.crawl()
    all_news.extend(billboard_scraper.news_data)

    # 将所有新闻保存到一个文件中
    if all_news:
        with open('allNews.json', 'w', encoding='utf8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=4)
        print(f"所有新闻数据已保存到 allNews.json")
    else:
        print("没有数据可保存")

if __name__ == "__main__":
    main()