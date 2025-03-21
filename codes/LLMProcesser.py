import json
import openai

class OpenAIProcessor:
    def __init__(self):
        openai.api_key = " sk-GXvHTdtNaBWUeuWcPBKxEo3tyBTfcbdKAq0gRVIzdfp6DDG4"
        openai.api_base = "https://api.chatanywhere.tech/v1"

    def extract_award_info(self, text):
        system_prompt = """
                        你是一个专业的科技奖项信息提取专家。
                        你的任务是从中国科技奖励文件中提取获奖信息，包括获奖人姓名、奖项类型、项目名称和所属单位。
                        请以JSON格式返回，确保JSON格式正确且只包含提取的信息。
        """

        user_prompt = f"""请从以下文本中对所有奖项进行处理,缺省默认为空.
        对于每个奖项，提取以下信息：
        1. 奖励省份 (prov)
        2. 奖励年份 (year)
        3. 项目名称 (proj)
        4. 获奖人姓名(name) (若有多个获奖人, 中间用空格隔开)
        5. 获奖人所在单位(unit) (若有多个单位, 中间用空格隔开)
        6. 提名单位(non_unit)
        7. 奖项类型，如自然科学奖, 技术发明奖, 科技进步奖等所有以奖结尾且不是奖励级别的条目 (type)
        8. 奖项级别, 如一等奖, 二等奖, 三等奖(level)

"""
        
        user_prompt += f"""请直接以有效的JSON数组格式返回,格式如下:
[
    {{
        "prov": "奖励省份",
        "year": "奖励年份",
        "proj": "项目名称", 
        "name": "获奖人姓名",
        'unit': "获奖人所在单位",
        'non_unit': "提名单位",
        "type": "奖项类型",
        "level": :奖项级别"
    }},
    ...
]

    如果文本中包含表格数据，请特别注意从表格中提取完整准确的信息。
    只返回JSON数组，不要包含其他文本。
    需要注意的是, 可能会有这样的情况:在输入的文本中, 先列出所有表格对应的奖励种类等再依次给出表格, 由于同一奖项的数目等同于该奖项下所有级别的最大编号的和，你需要尽可能匹配它们.
    另外, 若有无法确定的奖项类别等, 只要能确定获奖人的姓名, 你都需要将其输出, 其他部分默认为空
    最后, 虽然文本非常长, 你仍需要提取每一个奖项的对应信息, 即使这可能会花费很长时间.
    以下是需要分析的文本：
    {text}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1.0,  
                response_format={"type": "json_object"},  
                max_tokens=16000
            )
            
            result = response.choices[0].message.content
            with open("result.txt", "w") as f:
                 f.write(result)
            
            try:
                parsed_data = json.loads(result)
                if isinstance(parsed_data, dict):
                    for key in ["data", "awards", "results", "items"]:
                        if key in parsed_data and isinstance(parsed_data[key], list):
                            return parsed_data[key]
                    
                    for value in parsed_data.values():
                        if isinstance(value, list):
                            return value
                if isinstance(parsed_data, list):
                    return parsed_data
                
                print("无法从大模型的回复中提取数据列表")
                return []
                
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {str(e)}")
                try:
                    json_start = result.find('[')
                    json_end = result.rfind(']') + 1
                    if json_start != -1 and json_end != -1:
                        json_str = result[json_start:json_end]
                        return json.loads(json_str)
                except:
                    print("无法解析LLM返回的JSON数据")
                    return []
                
        except Exception as e:
            print(f"OpenAI API调用失败: {str(e)}")
            return []


def processTextWithLLM(text, LLM):
    if text:
        print("开始利用LLM提取信息...")
        try:
            datas = LLM.extract_award_info(text)
        except Exception as e:
            print(f"LLM提取信息失败:{e}")
            return 
        return datas
    else:
        print("未从页面提取出文本信息.")
        return