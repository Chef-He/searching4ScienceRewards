import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
from curl_cffi import requests

from getContent import getContent
from toExcel import toexcel
from LLMProcesser import*
#from getSuburl import getUrls

baseUrls = {
    "https://www.hainan.gov.cn/hainan/szfwj/202409/c92c25ae3746408eb3a336d97e453296.shtml",
    "非href: http://kjt.shandong.gov.cn/art/2019/12/27/art_13360_8494698.html",
    "处理pdf错误: https://kjt.shaanxi.gov.cn/gk/fdzdgknr/zcwj/qt/202103/t20210324_3366619.html"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

TARGET_KEYWORDS = ["名单", "获奖", "附件", "目录"] 

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

def needCheck(url):
    with open("M:\\MyLib\\000-temp\\url_to_check.txt", "a") as f:
        f.write(url + ' ')

def main():
    print("开始运行!")
    for baseUrl in baseUrls:
        try:
            urls = [baseUrl]
            for url in urls:
                text = search(url)
                if text:
                    print("开始利用LLM提取信息...")
                    try:
                        agent = OpenAIProcessor()
                    except Exception as e:
                        print(f"LLM初始化失败!{e}")
                        exit()
                    print("LLM准备完成!")
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
        except:
            continue
    print("结束!")

def main_url():
    pass
    print("开始运行!")
  #  urls =  getUrls(baseUrls[0])


if __name__ == "__main__":
    choice = int(input())
    if choice == 1:
        main()
    elif choice == 2:
        main_url()
