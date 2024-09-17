import json

# 打開並讀取JSON檔
with open('./simple_maze/maze_info.json', 'r') as f:
    data = json.load(f)

def get_maze_length(name= "length"):

    cols ,rows = data.get(name)

    return cols ,rows

def get_maze_border(name= "1_1"):
    row, col = name.split('_')
    if int(row) < 10:
        row = f'0{row}'
    if int(col) < 10:
        col = f'0{col}'
    name = f"{row}_{col}"

    value = data.get(name)

    return value

if  __name__ ==  '__main__':
    
    for row in range(1,11):
        for col in range(1,11):
            value = get_maze_border(f"{row}_{col}")
            print(f"{row}_{col}:", value)