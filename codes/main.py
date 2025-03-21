from seachInUrl import search
from LLMProcesser import *
from toExcel import toexcel
"""
    "非href: http://kjt.shandong.gov.cn/art/2019/12/27/art_13360_8494698.html",
    "处理pdf错误: https://kjt.shaanxi.gov.cn/gk/fdzdgknr/zcwj/qt/202103/t20210324_3366619.html"
"""
BASEUrl = {
    "https://www.hainan.gov.cn/hainan/szfwj/202409/c92c25ae3746408eb3a336d97e453296.shtml"
}
EXCELPATH = "M:\\MyLib\\200-Side_works\\204-TA\\scienceRewards.xlsx" 
CHECKPATH = "M:\\MyLib\\200-Side_works\\204-TA\\url_to_check.txt"

def main():
    print("开始运行!")
    try:
        LLM = OpenAIProcessor()
    except Exception as e:
        print(f"LLM初始化失败!{e}")
        exit() 
    print("LLM准备完成!")

    for url in BASEUrl:
        text = search(url)
        datas = processTextWithLLM(text, LLM)
        fail = toexcel(datas, EXCELPATH)
        if fail:   
            with open(CHECKPATH, "a") as f:
                f.write(url + '\n')

    print("结束!")



def main_test():
    pass

if __name__ == "__main__":
    choice = int(input("1:完整程序; 2:测试子函数\n"))
    if choice == 1:
        main()
    elif choice == 2:
        main_test()
