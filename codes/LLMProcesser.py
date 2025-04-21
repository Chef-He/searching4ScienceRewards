import json
import openai
import re

class OpenAIProcessor:
    def __init__(self):
        openai.api_key = " sk-GXvHTdtNaBWUeuWcPBKxEo3tyBTfcbdKAq0gRVIzdfp6DDG4"
        openai.api_base = "https://api.chatanywhere.tech/v1"
        self.system_prompt = """
            你是一个专业的中文科技奖项信息提取专家。
            你的任务是从中国科技奖励文件中提取获奖信息,包括获奖人姓名、奖项类型、项目名称和所属单位等。
            请以JSON格式返回,确保JSON格式正确且只包含提取的信息。
        """
        self.user_prompt = """
            你是一个专业的中文科技奖励信息抽取专家。请严格按照以下要求从文本中提取奖项信息:

            【任务说明】
            1. 请按文本中奖项出现的原始顺序逐个处理,确保不遗漏任何奖项中的任何项目.
            2. 每个奖项必须包含以下字段(若信息缺失请留空):
            - prov(省份)
            - year(年份) 
            - proj(项目名称)
            - name(获奖人,多人用空格分隔)
            - unit(所在单位,多个用空格分隔)
            - non_unit(提名单位, 注意不要与完成人单位混淆)
            - type(奖项类型, 注意不要包含奖励等级)
            - level(奖项等级)

            【处理规则】
            1. 按原始顺序处理每个奖项的每个项目,即使出现格式异常也要保留条目
            2. 信息提取优先级:
            a) 先匹配结构化字段(如括号标注的奖项类型)
            b) 再解析非结构化文本
            3. 遇到缺失字段时:
            - 保留条目框架
            - 对应字段设为空字符串""
            4. 处理多人/多单位时:
            - 保持原始顺序
            - 使用单个空格分隔
            5. 奖项类型标准化:
            - 匹配「」或《》中的内容
            - 若无标注,根据上下文推断

            【输出要求】
            1. 严格使用JSON数组格式
            2. 每个奖项对应一个对象
            3. 保持字段顺序:prov, year, proj, name, unit, non_unit, type, level
            4. 示例格式:
            [
            {
                "prov": "江苏省",
                "year": "2022",
                "proj": "量子通信关键技术研究",
                "name": "张三 李四",
                "unit": "南京大学 东南大学",
                "non_unit": "江苏省教育厅",
                "type": "技术发明奖",
                "level": "一等奖"
            }
            ]

            【强制措施】
            1. 必须处理所有可识别的奖项条目,不允许跳过任何奖项的任何项目.
            2. 每个处理步骤需自我验证:
            - 检查条目数量与原文匹配度
            - 验证必填字段完整性
            3. 将奖励类型与级别分开, 例如: 将"自然科学一等奖"分为"自然科学奖(type)"与"一等奖(level)".

            【强化指令】
            1. 必须采用线性逐行扫描方式处理文本, 对每个字符进行奖项起止标记检测
            2. 当检测到新奖项开始时立即创建条目框架, 即使后续字段可能不完整
            3. 每处理完3个条目后执行反向校验, 对照原文确认条目连续性

            请开始处理以下文本(请确保输出为有效JSON,不要添加任何注释):
        """

    def extract_award_info(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt + text}
                ],
                temperature=0.2,  
                response_format={"type": "json_object"},  
                max_tokens=16000
            )
            
            result = response.choices[0].message.content
            try:
                last_valid_obj_end = 0
                for match in re.finditer(r'\s*\{[^{}]*\}\s*,?', result, re.DOTALL):
                    last_valid_obj_end = match.end()
                
                if last_valid_obj_end > 0:
                    valid_part = re.sub(r',\s*$', '', result[:last_valid_obj_end])
                    result = f'{{\n{valid_part}\n]\n}}'[1:]
                    with open("json.txt", "w", encoding = "utf-8") as f:
                        f.write(result)
            
                parsed_data = json.loads(result)
                if isinstance(parsed_data, dict):
                    for key in ["data", "awards", "results", "items", "result"]:
                        if key in parsed_data and isinstance(parsed_data[key], list):
                            return parsed_data[key]
                
                print("无法从大模型的回复中提取数据列表")
                return []
                
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {str(e)}")

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