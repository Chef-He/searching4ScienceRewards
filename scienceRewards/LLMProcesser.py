import json
import openai

class OpenAIProcessor:
    def __init__(self):
        """初始化OpenAI API处理器"""
        openai.api_key = "sk-544e85b623f145878bf85c38362e8804"
        openai.api_base = "https://api.deepseek.com/v1"

    def extract_award_info(self, text):
        system_prompt = """
                        你是一个专业的科技奖项信息提取专家。
                        你的任务是从中国科技奖励文件中提取获奖信息，包括获奖人姓名、奖项类型、项目名称和所属单位。
                        请以JSON格式返回，确保JSON格式正确且只包含提取的信息。
        """

        # 构建用户提示
        user_prompt = f"""请从以下文本中提取所有科学技术奖项信息。

对于每个奖项，提取以下信息, 若有多个：
1. 奖励省份 (province)
2. 奖励年份 (year)
3. 项目名称 (project)
4. 获奖人姓名+所属单位(特别注意不是提名单位) (name_unit) (若有多个获奖人, 中间用空格隔开)
5. 奖项类型，如自然科学奖、科技进步奖等 (award_type)
6. 奖项级别, 如一等奖(award_level)

"""
        
        user_prompt += f"""请直接以有效的JSON数组格式返回，格式如下：
[
    {{
        "province": "奖励省份",
        "year": "奖励年份",
        "project": "项目名称", 
        "name_unit": "获奖人姓名(所属单位)",
        "award_type": "奖项类型",
        "award_level": :奖项级别"
    }},
    ...
]

如果文本中包含表格数据，请特别注意从表格中提取完整准确的信息。
只返回JSON数组，不要包含其他文本。

以下是需要分析的文本：
{text}"""

        try:
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model="deepseek-chat",  # 或其他适合的模型
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1.0,  # 低温度以获得更稳定的输出
                response_format={"type": "json_object"},  # 请求JSON格式返回
                max_tokens=4000
            )
            
            # 提取响应内容
            result = response.choices[0].message.content
            print(result)
            # 解析JSON
            try:
                # 尝试直接解析为JSON对象
                parsed_data = json.loads(result)
                
                # 检查是否有data或awards等外层键
                if isinstance(parsed_data, dict):
                    for key in ["data", "awards", "results", "items"]:
                        if key in parsed_data and isinstance(parsed_data[key], list):
                            return parsed_data[key]
                    
                    # 如果没有这些键但有一个列表值，返回它
                    for value in parsed_data.values():
                        if isinstance(value, list):
                            return value
                
                # 如果是列表，直接返回
                if isinstance(parsed_data, list):
                    return parsed_data
                
                print("无法从响应中提取数据列表")
                return []
                
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {str(e)}")
                # 尝试找到JSON部分
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
