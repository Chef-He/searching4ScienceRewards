from typing import List, Dict
from curl_cffi import requests

from fileConvert import doc_to_docx, pdf_to_docx, parse_docx

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def getContent(content_url: str) -> List[Dict[str, str]]:
   
    text =[]
    try:
        response = requests.get(content_url, headers=headers, timeout=15)
        response.raise_for_status()
        content = response.content

        if content_url.lower().endswith('.pdf'):
            try:
                print("检测到pdf, 开始转换")
                docx_bytes = pdf_to_docx(content)
                print("成功将pdf转为docx文档")
                try:
                    text = parse_docx(docx_bytes)
                except RuntimeError as e:
                    print(f"处理pdf文档时发生错误: {str(e)}")
            except Exception as e:
                print(f"失败:{str(e)}")
            
        elif content_url.lower().endswith(('.doc')):
            try:
                print("检测到doc, 开始转换")
                docx_bytes = doc_to_docx(content)
                print("成功将doc转为docx文档")
                try:
                    text = parse_docx(docx_bytes)
                except RuntimeError as e:
                    print(f"处理docx文档时发生错误: {str(e)}")
            except Exception as e:
                print(f"失败:{str(e)}")

        elif content_url.lower().endswith(('.docx')):
            try:
                text = parse_docx(content)
            except RuntimeError as e:
                print(f"处理docx文档时发生错误: {str(e)}")
        
        else:
            raise Exception("无法处理的文件类型")
    
    except Exception as e:
        print(f"处理失败: {str(e)}")
    
    finally:
        return text 