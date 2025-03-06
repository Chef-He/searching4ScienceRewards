import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
from curl_cffi import requests

from getContent import getContent
from toExcel import toexcel
from LLMProcesser import*

    #"https://sjt.zj.gov.cn/art/2024/12/18/art_1229563385_2539417.html",
    #"https://www.nmg.gov.cn/zwgk/zfgb/2017n_4768/201724/201711/t20171124_303996.html"

urls = [
    "https://www.gd.gov.cn/zwgk/gongbao/2021/15/content/post_3367214.html"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

TARGET_KEYWORDS = ["名单", "获奖", "科学技术奖", "附件", "目录"] 

def search(url):
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
                datas = getContent(full_url)
        
        return datas
                
    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时发生错误: {str(e)}")

    except Exception as e:
        print(f"处理 {url} 时发生意外错误: {str(e)}")

def needCheck(url):
    with open("M:\\MyLib\\000-temp\\url_to_check.txt", "a") as f:
        f.write(url + ' ')

def main():
    print("开始运行!")
    try:
        agent = OpenAIProcessor()
    except Exception as e:
        print(f"LLM初始化失败!{e}")
        exit()
    print("LLM准备完成!")
    for url in urls:
        text = search(url)
        if text:
            print("开始利用LLM提取信息...")
            datas = agent.extract_award_info(text)
            if datas:
                try:
                    print("开始将此次内容写入表格...")
                    toexcel(datas, 'M:\\MyLib\\000-Temp\\scienceRewards.xlsx')
                except:
                    print("写入失败!")
                    needCheck(url)
            else:
                print(f"LLM未返回任何值, 需要再次核实的url:{url}")
                needCheck(url)
        else:
            print(f"未从{url}中提取出任何信息, 请人工核实该网站")
            needCheck(url)

    print("结束!")

if __name__ == "__main__":
    main()