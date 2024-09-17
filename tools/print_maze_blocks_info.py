import json

maze_list = [[[0]*4]*20]*20

with open('maze_info.json', 'r') as f:
    data = json.load(f)
    data.pop("length")
    for key in data:
        maze_list[int(key.split('_')[0])-1][int(key.split('_')[1])-1] = [1-x for x in data[key]]
    data = str(data)

print(maze_list)