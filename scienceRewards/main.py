import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
from getContent import getContent
from toExcel import toexcel
# 配置参数
    #"https://sjt.zj.gov.cn/art/2024/12/18/art_1229563385_2539417.html",
urls = [
    "https://www.gd.gov.cn/zwgk/gongbao/2021/15/content/post_3367214.html",
    "https://www.nmg.gov.cn/zwgk/zfgb/2017n_4768/201724/201711/t20171124_303996.html"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 定义要匹配的关键词列表
TARGET_KEYWORDS = ["名单", "获奖", "科学技术奖", "附件"]  # 根据需求自行修改

def search(url):
    """
    :param url: 当前处理的页面URL
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"\n正在分析页面: {url}")
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有<a>标签
        for link in soup.find_all('a'):
            # 获取链接显示文本（去除首尾空白）
            link_text = link.get_text(strip=True)
            # 获取原始href属性
            raw_href = link.get('href', '')

            # 检查链接文本是否包含任意目标关键词
            if any(keyword in link_text for keyword in TARGET_KEYWORDS):
                print(f"发现目标链接: [{link_text}] -> {raw_href}")
                
                # 构建完整URL（处理相对路径）
                full_url = urljoin(url, raw_href)
                
                # 执行内容处理操作
                datas = getContent(full_url)

                if datas:
                    toexcel(datas, 'M:\\MyLib\\000-Temp\\scienceRewards.xlsx')
                sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时发生错误: {str(e)}")

    except Exception as e:
        print(f"处理 {url} 时发生意外错误: {str(e)}")

if __name__ == "__main__":
    print("Start!")
    for url in urls:
        search(url)
    print("Done!")