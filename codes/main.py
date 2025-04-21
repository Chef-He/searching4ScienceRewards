from seachInUrl import search
from LLMProcesser import *
from toExcel import toexcel
"""
    
"""
BASEUrl = {
    "https://www.sc.gov.cn/10462/zfwjts/2023/3/28/3240ed4c95244d088967c07ec7c914df.shtml"
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
        search(url)
        print("读入完成!")
        """
        full_datas = []
        with open("table.txt", "r", encoding = "utf-8") as f:
            heading = f.readline() + '\n'
            lines = f.readlines()
            chunk_items = len(lines) // 5 + 1
            for i in range(5):
                start_line = i * chunk_items
                end_line = min(len(lines), (i + 1) * chunk_items)
                text = heading + '\n'.join(lines[start_line:end_line])
                datas = processTextWithLLM(text, LLM)
                full_datas.extend(datas)
        print(len(full_datas))
        exit()
        toexcel(full_datas, EXCELPATH)
        """
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
    choice = input("执行写入?[y/n]\n")
    if choice == 'y':
        toexcel(datas, EXCELPATH)

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
    choice = int(input("1:从url中获取str并存入table.txt\n2:从table.txt推理json字符并写入excel\n3: 从json.txt中的json字段输入excel\n"))
    if choice == 1:
        main()
    elif choice == 2:
        main_test()
    elif choice == 3:
        main_test2()