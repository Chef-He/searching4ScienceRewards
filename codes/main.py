from seachInUrl import search
from LLMProcesser import *
from toExcel import toexcel
"""
    "非href: http://kjt.shandong.gov.cn/art/2019/12/27/art_13360_8494698.html"
    "https://www.hainan.gov.cn/hainan/szfwj/202409/c92c25ae3746408eb3a336d97e453296.shtml"
    "处理为docx后无产出:https://kjt.shaanxi.gov.cn/gk/fdzdgknr/zcwj/qt/202103/t20210324_3366619.html"
    广东2020"https://www.gd.gov.cn/zwgk/gongbao/2021/15/content/post_3367214.html",
     广东2023"https://www.gd.gov.cn/zzzq/zxzc/content/post_4509595.html"
"""
BASEUrl = {
    "https://www.shanghai.gov.cn/nw12344/20210525/79ba956915b946a5b46f00ef63957f07.html"
}
EXCELPATH = "M:\\MyLib\\200-Side_works\\204-TA\\scienceRewards.xlsx" 
CHECKPATH = "M:\\MyLib\\200-Side_works\\204-TA\\url_to_check.txt"

def main():
    print("开始运行!")
    """
    try:
        LLM = OpenAIProcessor()
    except Exception as e:
        print(f"LLM初始化失败!{e}")
        exit() 
    print("LLM准备完成!")
    """
    for url in BASEUrl:
        text = search(url)
        print("读入完成, 结束!")
        continue
    """
        datas = processTextWithLLM(text, LLM)
        fail = toexcel(datas, EXCELPATH)
        if fail:   
            with open(CHECKPATH, "a") as f:
                f.write(url + '\n')

    print("结束!")
    """

def main_test():
    with open("table.txt", "r", encoding="utf-8") as f:
        text = f.read()
    LLM = OpenAIProcessor()
    datas = processTextWithLLM(text, LLM)
    print(f"接受到{len(datas)}条数据, 请核实")

def main_test2():
    with open("json.txt", "r", encoding = "utf-8") as f:
        result = f.read()
    parsed_data = json.loads(result)
    if isinstance(parsed_data, dict):
        for key in ["data", "awards", "results", "items", "result"]:
            if key in parsed_data and isinstance(parsed_data[key], list):
                datas = parsed_data[key]
        toexcel(datas, EXCELPATH)

if __name__ == "__main__":
    choice = int(input("1:完整程序\n2:从table.txt推理json字符并写入excel\n3: 从json.txt中的json字段输入excel\n"))
    if choice == 1:
        main()
    elif choice == 2:
        main_test()
    elif choice == 3:
        main_test2()