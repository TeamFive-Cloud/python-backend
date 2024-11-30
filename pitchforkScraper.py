import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class PitchforkScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        self.reviews_data = []

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

    def parse_pitchfork(self, html_content):
        """解析 pitchfork.com 音乐评论"""
        soup = BeautifulSoup(html_content, 'html.parser')
        review_items = soup.select('div.SummaryItemWrapper-iwvBff')  # 根据实际的HTML结构调整选择器
        
        for item in review_items:
            try:
                title = item.select_one('h3.SummaryItemHedBase-hiFYpQ').get_text().strip() if item.select_one('h3.SummaryItemHedBase-hiFYpQ') else 'N/A'
                artist = item.select_one('div.SummaryItemSubHedBase-gMyBBg').get_text().strip() if item.select_one('div.SummaryItemSubHedBase-gMyBBg') else 'N/A'
                description = item.select_one('div.SummaryItemDek-CRfsi').get_text().strip() if item.select_one('div.SummaryItemDek-CRfsi') else 'N/A'
                img_tag = item.select_one('img.ResponsiveImageContainer-eybHBd')
                img_url = img_tag['src'] if img_tag else 'N/A'
                link = "https://pitchfork.com" + item.select_one('a.SummaryItemHedLink-civMjp')['href']
                date = item.select_one('time.SummaryItemBylinePublishDate-ctLSIQ').get_text().strip() if item.select_one('time.SummaryItemBylinePublishDate-ctLSIQ') else 'N/A'
                
                self.reviews_data.append({
                    'source': 'Pitchfork',
                    'title': title,
                    'artist': artist,
                    'description': description,
                    'img_url': img_url,
                    'link': link,
                    'date': date
                })
                print(f"成功解析评论: {title} by {artist}")
            except Exception as e:
                print(f"解析Pitchfork评论出错: {str(e)}")
                continue

    def crawl(self):
        """爬取 pitchfork.com 网站的音乐评论"""
        url = 'https://pitchfork.com/best/'
        html_content = self.fetch_page(url)
        
        if html_content:
            self.parse_pitchfork(html_content)
        
        # 添加随机延迟
        time.sleep(random.uniform(2, 4))

def main():
    all_reviews = []

    pitchfork_scraper = PitchforkScraper()
    pitchfork_scraper.crawl()
    all_reviews.extend(pitchfork_scraper.reviews_data)

    # 将所有评论保存到一个文件中
    if all_reviews:
        with open('pitchforkReviews.json', 'w', encoding='utf8') as f:
            json.dump(all_reviews, f, ensure_ascii=False, indent=4)
        print(f"所有评论数据已保存到 pitchforkReviews.json")
    else:
        print("没有数据可保存")

if __name__ == "__main__":
    main()