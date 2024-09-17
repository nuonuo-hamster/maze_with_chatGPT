from openai import OpenAI
import json
import base64

def encode_image(image_path):
    with open(image_path,'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
client = OpenAI()

image_path = './maze.jpg'
maze_list = [[[0]*4]*20]*20

base64_image = encode_image(image_path)

with open('maze_info.json', 'r') as f:
    data = json.load(f)
    data.pop("length")
    for key in data:
        maze_list[int(key.split('_')[0])-1][int(key.split('_')[1])-1] = [1-x for x in data[key]]
    data = str(data)

messages = [
    {"role": "system", "content": 'You are a maze solver' },
    {"role": "user", "content": [
            {"type": "text", "text": "這是一張20*20格迷宮圖片，每格大小為40*40pixel" },
            {
                "type": "image_url",
                "image_url": {
                "url": f'data:image/jpeg;base64,{base64_image}'
                    },
            },
        ],
    },
    {"role": "user", "content": '最左上格編號是(1,1) 最右上格編號是(1,20) 最左下格編號是(20,1) 最右下格編號是(20,20)' },
    {"role": "user", "content": '找到從(1,1)走到(20,20)的路徑' },
]

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    max_tokens=300,
)
print(completion.choices[0].message.content)