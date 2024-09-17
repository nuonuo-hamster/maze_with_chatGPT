from openai import OpenAI
import json

client = OpenAI()

with open('maze_info.json', 'r') as f:
    data = json.load(f)
    data.pop("length")
    for key in data:
        data[key] = [1-x for x in data[key]]

messages = [
    {"role":"system","content":"You are a maze-solving robot."},
    {"role": "user", "content": "有一個20乘以20的迷宮，資訊如下:"},
    {"role": "user", "content": f"data: {data}"},
    {"role": "user", "content": "data.key 代表著(橫列row編號)_(縱列column編號)"},
    {"role": "user", "content": "data.value 代表著[上方是(1)否(0)能通過,下方是否能通過,左方是否能通過,右方是否能通過]"},
    {"role": "user", "content": "求出從01_01到達20_20的可行路線，以行經的(row)_(column)->形式回答"},
    ]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=200,
)
print(completion.choices[0].message.content)