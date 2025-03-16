import openpyxl
import os
from openpyxl.styles import Alignment
from typing import List, Dict

def toexcel(datas: List[Dict], file: str):
    items = 0
    file_exists = os.path.exists(file)

    if file_exists:
        wb = openpyxl.load_workbook(file, read_only=False)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["省份", "年份", "项目", "获奖人员", "奖励类型", "奖励级别"])  
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            cell = ws[f"{col}1"]
            cell.alignment = Alignment(horizontal='center')

    try:
        for data in datas:
            ws.append([
                data.get("province", ""),  
                data.get("year", ""),      
                data.get("project", ""),    
                data.get("name_unit", ""),    
                data.get("award_type", ""),
                data.get("award_level", "")
            ])
            items += 1

        column_widths = {
        'D': 75,
        'C': 50, 
        'E': 25
    }
    
        for column, width in column_widths.items():
            ws.column_dimensions[column].width = width

        wb.save(file)
        print(f"{items}条数据已写入至 {file}")
        
    except Exception as e:
        print(f"写入数据时发生错误: {str(e)}")
    finally:
        wb.close()