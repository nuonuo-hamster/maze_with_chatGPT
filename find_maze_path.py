import os
import json
from collections import deque

maze_file = './maze_info.json'
route_file = './route_info.json'

def load_maze(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def find_best_path(maze, start_end):

    start, end = start_end
    rows, cols = 20, 20  # Assuming a 20x20 maze; modify as needed
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        (current, path) = queue.popleft()
        current_r, current_c = current
        
        if current == end:
            pass
            return path + [current]
        
        for dr, dc in directions:
            next_r, next_c = current_r + dr, current_c + dc
            if 1 <= next_r <= rows and 1 <= next_c <= cols:
                next_cell = f"{next_r:02}_{next_c:02}"
                if next_cell not in visited and (dr == 0 and (dc == 1 and maze[f"{current_r:02}_{current_c:02}"][3] == 0) or
                                                 (dc == -1 and maze[f"{current_r:02}_{current_c:02}"][2] == 0) or
                                                 (dr == 1 and (dc == 0 and maze[f"{current_r:02}_{current_c:02}"][1] == 0)) or
                                                 (dr == -1 and (dc == 0 and maze[f"{current_r:02}_{current_c:02}"][0] == 0))):
                    queue.append(((next_r, next_c), path + [current]))
                    visited.add(next_cell)
    return None

def find_longest_path(maze, start, end):
    rows, cols = 20, 20  # 假设迷宫是 20x20 的，必要时可以修改
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上

    def is_valid_move(current_r, current_c, dr, dc):
        next_r, next_c = current_r + dr, current_c + dc
        if 1 <= next_r <= rows and 1 <= next_c <= cols:
            next_cell = f"{next_r:02}_{next_c:02}"
            if next_cell in maze:
                if (dr == 0 and (dc == 1 and maze[f"{current_r:02}_{current_c:02}"][3] == 0) or
                    (dc == -1 and maze[f"{current_r:02}_{current_c:02}"][2] == 0)) or \
                   (dr == 1 and (dc == 0 and maze[f"{current_r:02}_{current_c:02}"][1] == 0)) or \
                   (dr == -1 and (dc == 0 and maze[f"{current_r:02}_{current_c:02}"][0] == 0)):
                    return True
        return False

    longest_path = []
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()
        current_r, current_c = current

        if current == end:
            if len(path) > len(longest_path):
                longest_path = path
        
        visited.add(current)

        for dr, dc in directions:
            next_r, next_c = current_r + dr, current_c + dc
            next_cell = (next_r, next_c)
            if next_cell not in visited and is_valid_move(current_r, current_c, dr, dc):
                stack.append((next_cell, path + [next_cell]))
    
    return longest_path

def append_route_to_json(route_filename, start_end_color, path):
    
    start_color, end_color = start_end_color

    route_key = f"{start_color}_to_{end_color}"
    
    # 将路径转换为指定的元组格式
    route_value = [(f"{step[0]:02}_{step[1]:02}") for step in path]
    
    # 如果 route.json 文件不存在，创建一个空的字典
    if not os.path.exists(route_filename):
        route_data = {}
    else:
        with open(route_filename, 'r') as f:
            route_data = json.load(f)
    
    # 添加路径到 route_data 中
    route_data[route_key] = route_value
    
    # 将更新后的数据保存回 route.json 文件
    with open(route_filename, 'w') as f:
        json.dump(route_data, f, indent=4)

def get_path(start_end, start_end_color):

    maze = load_maze(maze_file)
    path = find_best_path(maze, start_end)
    # path = find_longest_path(maze, start, end)
    
    if path:
        # print("路径找到！经过的路径是：")
        # for step in path:
        #     print(f"{step[0]:02}_{step[1]:02}")
        # print("路径找到！路径已追加到 route.json 文件中。")
        append_route_to_json(route_file, start_end_color, path)
    else:
        print("无法找到从起点到终点的路径。")

    steps = len(path)
    return steps

if __name__ == "__main__":

    steps = get_path(((1,1), (20,20)), ("startColor", "endColor"))
    print(f"steps: {steps}")