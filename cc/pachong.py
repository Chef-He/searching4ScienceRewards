import pymysql
import requests
import logging
import re
import urllib.request, urllib.error
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists
import random
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Generation # type: ignore
BASE_URL = 'https://movie.douban.com/top250'
TOTAL_PAGE = 2
RESULTS_DIR = 'results'
def scrape_index(page):
    index_url = f'{BASE_URL}?start={(page - 1) * 25}'
                                                     #每页有二十五个电影，所以翻页逻辑
    return askURL(index_url)

def parse_index(html):
    pattern = re.compile(r'<a href="(https://movie.douban.com/subject/\d+/)" class="">')
     
    items = re.findall(pattern,html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url
                                                          #进入子页面（详情页）
def comments_sonpage(web,i):                              # 返回每个评论页的html
    comment_index=f'{web}comments?start={i*20}&limit=20&status=P&sort=new_score'   
    #print(f'{web}comments?start={i*20}&limit=20&status=P&sort=new_score') 
    return askURL(comment_index)


def comments_detail(html):
    comment_pattern=re.compile(r'<span class="short">(.*?)</span>',re.S)
    cd=re.findall(comment_pattern, html)
    return cd

def parse_detail(html):
    name_pattern= re.compile(r'<span property="v:itemreviewed">(?P<name>.*?)</span>', re.S)
    #year_pattern= re.compile(r'<span class="year">(?P<year>.*?)</span>',re.S)
    #director_pattern=re.compile(r'<a href=".*?" rel="v:directedBy">(.*?)</a>', re.S)
    #author_pattern=re.compile(r'<a href=".*?" rel="v:directedBy">.*?</a>.*?<a href=".*?">(.*?)</a>', re.S)
    #author_pattern=re.compile(r'<span>.*?<span class="pl">.*?</span>: <span class="attrs">.*?<a href="https://www.douban.com/personage.*?">(.*?)</a>', re.S)
    #author_pattern=re.compile(r'<span class="pl">.*?</span>: <span class="attrs">.*?<a href="c.*?">(.*?)</a>', re.S)
    #short_pattern=re.compile(r'<span class="short">(.*?)</span>')

#分别抓取各项信息


    name=re.findall(name_pattern, html) 
    #director=re.findall(director_pattern, html)
    #year=re.findall(year_pattern, html)
    #author=re.findall(author_pattern, html)
    #short=re.findall(short_pattern,html)
    #return {'director':director,'name':name,'year':year,'author':author,'short commentary':short



    #}
    return name
def save_data(data):
    '''data_path = f'{RESULTS_DIR}/test1.json' # 保存文件的路径，可以根据需要修改文件名
    with open(data_path, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)'''
    #data1=json.dumps(data)
     
    #name = data.get('name')
    #data_path = f'{RESULTS_DIR}/{name}.json'

    data_path = f'{RESULTS_DIR}/test1.json'
    with open('moviecomments.json','w',encoding='utf-8')as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    #先把所有信息存到一个列表里，再一起存入json文件
def askURL(url):
    head = { 
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    #伪装成浏览器去访问

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
   
        


    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
       
    return html
def main():
    data={}
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        
        for detail_url in detail_urls:
            cd=[]
            for i in range(3,5):
                comment_html=comments_sonpage(detail_url,i)
                cd+=comments_detail(comment_html)
                

                
                
            detail_html = askURL(detail_url)
            mname=parse_detail(detail_html)
            data[mname[0]]=cd
            print(data)
           
    save_data(data)


if __name__ == '__main__':
    main()
