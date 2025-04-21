import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from curl_cffi import requests, Curl, CurlOpt

from getContent import getContent

def search(url):
    #--从url中得到文件,并提取文件中的信息(str)--
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    TARGET_KEYWORDS = ["附件", "目录", "清单", "公告", "项目", "获奖", "名单"] 
    datas = []
    try:
        response = requests.get(url, headers=headers, timeout=10) 
        response.raise_for_status()
        print(f"\n正在分析页面: {url}")
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            link_text = link.get_text(strip=True)
            raw_href = link.get('href', '')

            if any(keyword in link_text for keyword in TARGET_KEYWORDS):
                print(f"发现目标链接: [{link_text}] -> {raw_href}")
                full_url = urljoin(url, raw_href)
                try:
                    datas = getContent(full_url)
                    if datas:
                        return datas
                except: 
                    continue
                
    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时发生错误: {str(e)}")

    except Exception as e:
        print(f"处理 {url} 时发生意外错误: {str(e)}")
    
    finally:
        return datas
    