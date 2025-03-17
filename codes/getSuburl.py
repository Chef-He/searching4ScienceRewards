import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from typing import List

def getUrls(base_url: str) -> List[str]:
   
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GovBot/1.0',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    TIMEOUT = 10
    MAX_DEPTH = 2
    
    TITLE_PATTERN = re.compile(
        r'^([\u4e00-\u9fa5]{2,5}省|自治区|市)人民政府关于(\d{4})年度*科学技术奖励的通告$'
    )
    
    URL_KEYWORDS = [
        'zwgk',    
        'tzgg',    
        'gsgg',    
        'zfxxgk',
        'kjcg',    
        'kjcx'     
    ]
    
    def crawl_site(url: str, depth: int, visited: set) -> set:
        if depth > MAX_DEPTH or url in visited:
            return set()
        
        visited.add(url)
        matched_urls = set()
        
        try:
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=3)
            session.mount('https://', adapter)
            
            response = session.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)
            response.encoding = 'utf-8'  
            soup = BeautifulSoup(response.text, 'lxml')
            
            title_tag = soup.find('title')
            if title_tag and TITLE_PATTERN.match(title_tag.text.strip()):
                return {url}
            
            for link in soup.find_all('a', href=True):
                href = link['href'].strip()
                full_url = urljoin(url, href)
                
                if not is_valid_url(full_url):
                    continue
                
                path = urlparse(full_url).path.lower()
                if any(kw in path for kw in URL_KEYWORDS):
                    matched_urls.update(crawl_site(full_url, depth+1, visited))
                    
        except Exception as e:
            print(f"抓取失败 {url}: {str(e)}")
            
        return matched_urls
    
    def is_valid_url(url: str) -> bool:
        parsed = urlparse(url)
        return (
            parsed.scheme in ('http', 'https') and
            parsed.netloc == urlparse(base_url).netloc and
            not parsed.path.endswith(('pdf', 'doc', 'docx')) and
            'login' not in parsed.path
        )
    
    try:
        sitemap_url = urljoin(base_url, '/sitemap.xml')
        sitemap_links = parse_sitemap(sitemap_url) if check_sitemap(sitemap_url) else []
        
        crawled_urls = crawl_site(base_url, 0, set())
        return list(crawled_urls.union(sitemap_links))
    
   