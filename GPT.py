from openai import OpenAI
import time

class GPT():
    def __init__(self, api_key,
                 base_url = "https://api.moonshot.cn/v1",):
        self.api_key = api_key
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.model = "moonshot-v1-8k"
        self.temperature = 0.3
        self.messages = [
            {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
        ]
        self.prompt = "接下来有一道题目，你需要尝试回答，这个题的题目是{}, 选项是{}, 不同的选项使用换行符分隔\
            , 它是一个{}, \
        你需要找出符合题意的答案并复述，\
        ，不要回答多余的内容，只要复述正确选项内容即可，如果有多个答案，每个答案用#分隔，单选题和判断题都只有一个答案"
    def get_anwser(self, info, temperature=0.3):
        if info['type'] == 'judgement':
            info['type'] = "判断题"
        elif info['type'] == 'single':
            info['type'] = "单选题"
        elif info['type'] == 'multiple':
            info['type'] = "多选题"
            
        self.messages[0]["content"] = self.prompt.format(info["title"], info["options"], info["type"])
        try:
            completion = self.client.chat.completions.create(
                model = self.model,
                messages = self.messages,
                temperature = temperature,)
        except Exception as e:
            time.sleep(5)
            completion = self.client.chat.completions.create(
            model = self.model,
            messages = self.messages,
            temperature = temperature,)
        if " " in completion.choices[0].message.content or "#" in completion.choices[0].message.content and (info['type'] == "判断题" or info['type'] == "单选题"):
            return completion.choices[0].message.content.split(" ")[0].split("#")[0]
        return completion.choices[0].message.content







