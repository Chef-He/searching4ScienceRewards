import openpyxl
import os
from openpyxl.styles import Alignment
from typing import List, Dict

def toexcel(datas: List[Dict], file: str):
    """将数据写入 Excel 文件"""
    # 检查文件是否存在
    file_exists = os.path.exists(file)

    # 创建一个工作簿
    if file_exists:
        # 如果文件存在，加载工作簿
        wb = openpyxl.load_workbook(file)
        ws = wb.active
    else:
        # 如果文件不存在，创建一个新的工作簿和表头
        wb = openpyxl.Workbook()
        ws = wb.active
        # 写入表头
        ws.append(["省份", "年份", "奖励", "获奖人", "项目", "所属单位"])  
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            cell = ws[f"{col}1"]
            cell.alignment = Alignment(horizontal='center')

    # 写入数据
    try:
        for data in datas:
            ws.append([
                data.get("province", ""),  # 省份
                data.get("year", ""),      # 年份
                data.get("award_type", ""),# 奖励
                data.get("name", ""),      # 获奖人
                data.get("project", ""),    # 项目
                data.get("unit", "")       # 所属单位
            ])

        # 保存文件
        column_widths = {
        'D': 150,  # 获奖人
        'E': 50,  # 项目
        'F': 150 # 所属单位
    }
    
        for column, width in column_widths.items():
            ws.column_dimensions[column].width = width

        wb.save(file)
        print(f"数据已写入至 {file}")
    except Exception as e:
        print(f"写入数据时发生错误: {str(e)}")
    finally:
        wb.close()