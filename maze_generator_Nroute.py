import json
import random

def initialize_maze(rows, cols):
    maze = {}
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            key = f"{r:02}_{c:02}"
            # 初始化每个格子四个方向都有黑线
            maze[key] = [1, 1, 1, 1]  # 上, 下, 左, 右
    return maze

def remove_wall(maze, r1, c1, r2, c2):
    key1 = f"{r1:02}_{c1:02}"
    key2 = f"{r2:02}_{c2:02}"
    if r1 == r2:
        if c1 < c2:
            maze[key1][3] = 0
            maze[key2][2] = 0
        else:
            maze[key1][2] = 0
            maze[key2][3] = 0
    elif c1 == c2:
        if r1 < r2:
            maze[key1][1] = 0
            maze[key2][0] = 0
        else:
            maze[key1][0] = 0
            maze[key2][1] = 0

def generate_maze(rows, cols):
    maze = initialize_maze(rows, cols)
    
    # 确保最外圈都是黑线，除了入口和出口
    for r in range(1, rows + 1):
        if r != 1:
            maze[f"{r:02}_01"][2] = 1  # 左边
        if r != rows:
            maze[f"{r:02}_{cols:02}"][3] = 1  # 右边
    
    for c in range(1, cols + 1):
        if c != 1:
            maze[f"01_{c:02}"][0] = 1  # 上边
        if c != cols:
            maze[f"{rows:02}_{c:02}"][1] = 1  # 下边
    
    # 确定入口和出口
    entrance = (1, 1)
    exit = (rows, cols)
    
    # 使用深度优先搜索生成主路径
    stack = [entrance]
    visited = set()
    visited.add(entrance)
    
    while stack:
        current = stack[-1]
        r, c = current
        neighbors = []
        
        if r > 1 and (r-1, c) not in visited:
            neighbors.append((r-1, c))
        if r < rows and (r+1, c) not in visited:
            neighbors.append((r+1, c))
        if c > 1 and (r, c-1) not in visited:
            neighbors.append((r, c-1))
        if c < cols and (r, c+1) not in visited:
            neighbors.append((r, c+1))
        
        if neighbors:
            next_cell = random.choice(neighbors)
            stack.append(next_cell)
            visited.add(next_cell)
            remove_wall(maze, r, c, next_cell[0], next_cell[1])
        else:
            stack.pop()
    
    # 确保有一条路径到达出口
    if exit not in visited:
        return generate_maze(rows, cols)  # 重新生成迷宫
    
    # 生成副路径
    all_cells = list(maze.keys())
    for cell in all_cells:
        if cell != f"{entrance[0]:02}_{entrance[1]:02}" and cell != f"{exit[0]:02}_{exit[1]:02}":
            r, c = map(int, cell.split('_'))
            if random.random() < 0.2:  # 20% 概率添加副路径
                neighbors = []
                if r > 1:
                    neighbors.append((r-1, c))
                if r < rows:
                    neighbors.append((r+1, c))
                if c > 1:
                    neighbors.append((r, c-1))
                if c < cols:
                    neighbors.append((r, c+1))
                if neighbors:
                    next_cell = random.choice(neighbors)
                    remove_wall(maze, r, c, next_cell[0], next_cell[1])
    
    return maze

#########################
def main():
    # 生成20x20的迷宫
    rows, cols = 20, 20
    # start = (1, 1)  # 起点
    # end = (20, 20)  # 终点

    maze_data = generate_maze(rows, cols)
    maze_data['length'] = [rows, cols]
    route_data = {}

    with open('./maze_info.json', 'w') as f:
        json.dump(maze_data, f, indent=4)
    
    with open('./route_info.json', 'w') as f:
        json.dump(route_data, f, indent=4)

    print("迷宫已生成并保存到 maze.json 文件中。")

if __name__ == "__main__":
    main()
