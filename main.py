import json
import print_maze
import find_maze_path

with open('route_info.json', 'r') as f:
    data = json.load(f)

def print_movement(route_list):
        
    x1 = [int(route_list[0].split('_')[0]), int(route_list[0].split('_')[1])]
    for i in range(len(route_list)-1):

        x2 = [int(route_list[i+1].split('_')[0]), int(route_list[i+1].split('_')[1])]

        print(f"{i+1}", end=': ')
        if (x2[0]-x1[0]) == -1: print("up")
        if (x2[0]-x1[0]) ==  1: print("down")
        if (x2[1]-x1[1]) ==  1: print("right")
        if (x2[1]-x1[1]) == -1: print("left")

        x1 = x2

def analyse_route(name):

    route_list = data.get(name)
    steps = len(route_list) -1
    print(name.split('to')[0], 'to', name.split('to')[1])
    print("Total",steps,"steps")

    print_movement(route_list)
    
def N_to_M_lister():
    start = (6 ,18)
    end = (14, 7)
    analyse_route(name=f"{str(start[0]).zfill(2)}_{str(start[1]).zfill(2)}to{str(end[0]).zfill(2)}_{str(end[1]).zfill(2)}")

def draw_maze_only_checkpoint(checkpoints):
    print_maze.raw_map_printer(checkpoints)

def find_checkpoints_route(checkpoints):

    num_checkpoints = len(checkpoints)
    for i in range(0, num_checkpoints):
        start_color = list(checkpoints)[i]
        for j in range(i+1, num_checkpoints):
            end_color = list(checkpoints)[j]

            start = checkpoints[start_color]
            end = checkpoints[end_color]
            steps = find_maze_path.get_path((start, end), (start_color, end_color))
            print(f"{start_color}_to_{end_color}: {start} to {end}")
            print(f"steps: {steps}")

if __name__ in '__main__':

    checkpoints = {'green':(10,10),'purple':(1,1),'yellow':(16,5)
              ,'pink':(3,17),'blue':(20,20)}
    
    
    #塗checkpoint方塊, 顯示
    # draw_maze_only_checkpoint(checkpoints)

    #算距離 1-2 1-3 1-4 1-5 2-3 2-4 2-5 3-4 3-5 4-5
    find_checkpoints_route(checkpoints)
    

    #### print_maze.route_map_printer(start="06_18", end="14_07")
    #問chatGPT 優先級，最短距離，出發點，終點
    #集合紅區 顯示 重疊淺紅深紅，淺綠淺藍