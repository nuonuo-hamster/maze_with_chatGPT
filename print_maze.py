import cv2
import numpy as np
import extractJson
import find_maze_path

maze_file = './maze_info.json'
route_file = './route_info.json'
blocks_list = []

def route_printer(block, row, col, enter, exist, fpath_finder):

    maze = find_maze_path.load_maze(maze_file)

    start = (int(enter.split('_')[0]), int(enter.split('_')[1]))
    end = (int(exist.split('_')[0]), int(exist.split('_')[1]))

    path = fpath_finder(maze, start, end)
    
    find_maze_path.append_route_to_json(route_file, start, end, path)

    if (row, col) in path:
        block[:, :, 0] = 0
        block[:, :, 1] = 0
        block[:, :, 1] = 255

    return block

def checkpoint_printer(block, row, col, checkpoints):

    is_checkpoint = False
    color = ''

    for key, value in checkpoints.items():
        if (row,col) == value:
            is_checkpoint = True
            color = key
            break
    
    if(not is_checkpoint): return block

    if color == "yellow":
        block[:, :, 0] = 0
        block[:, :, 1] = 150
        block[:, :, 2] = 150
    if color == "green":
        block[:, :, 0] = 0
        block[:, :, 1] = 100
        block[:, :, 2] = 0
    if color == "blue":
        block[:, :, 0] = 100
        block[:, :, 1] = 0
        block[:, :, 2] = 0
    if color == "pink":
        block[:, :, 0] = 147
        block[:, :, 1] = 20
        block[:, :, 2] = 255
    if color == "purple":
        block[:, :, 0] = 128
        block[:, :, 1] = 0
        block[:, :, 2] = 128

    return block

def generate_blocks(rows, cols, checkpoints, route=False, enter=None, exist=None, fpath_finder=None):

    for row in range(1,rows+1):
        for col in range(1,cols+1):
            # 創建一個40x40全白(255)的圖片
            white_image = np.ones((40, 40, 3), dtype=np.uint8) * 255

            if route == True:
                white_image = route_printer(white_image, row, col, enter, exist, fpath_finder)
            
            white_image = checkpoint_printer(white_image, row, col, checkpoints)

            # 設置黑色邊緣的厚度
            border_thickness = 5

            up, down, left, right = extractJson.get_maze_border(f"{row}_{col}")
            # 在圖片的上方繪製一條黑色的線作為邊框
            if up:
                cv2.line(white_image, (0, 0), (white_image.shape[1]-1, 0), (0, 0, 0), border_thickness)

            if down:
                cv2.line(white_image, (0, white_image.shape[0]-1), (white_image.shape[1]-1, white_image.shape[0]-1), (0, 0, 0), border_thickness)
            
            if left:
                cv2.line(white_image, (0, 0), (0, white_image.shape[0]-1), (0, 0, 0), border_thickness)
            
            if right:
                cv2.line(white_image, (white_image.shape[1]-1, 0), (white_image.shape[1]-1, white_image.shape[0]-1), (0, 0, 0), border_thickness)

            blocks_list.append(white_image)

def contact_blocks(rows, cols):

    # 獲取單個圖像的尺寸（假設所有圖像尺寸相同）
    img_height, img_width, img_channels = blocks_list[0].shape

    # 創建空白的大圖片來容納所有子圖像
    stitched_image = np.zeros((img_height * rows, img_width * cols, img_channels), dtype=np.uint8)

    # 逐行逐列填充圖像
    for i in range(rows):
        for j in range(cols):
            # 計算當前圖像在輸出圖像中的位置
            stitched_image[i*img_height:(i+1)*img_height, j*img_width:(j+1)*img_width] = blocks_list[i * cols + j]

    return stitched_image

def print_img(img, save=False):

    # 顯示圖片
    cv2.imshow('White Image with Top Border', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存圖片到文件
    if save:
        cv2.imwrite('maze.jpg', img)

def raw_map_printer(checkpoints):

    cols, rows = extractJson.get_maze_length()
    generate_blocks(cols, rows, checkpoints, route=False)
    contact_image = contact_blocks(rows, cols)
    print_img(img = contact_image, save=True)

def route_map_printer(start, end, checkpoints):

    cols, rows = extractJson.get_maze_length()

    path_finder = find_maze_path.find_best_path
    # path_finder = find_maze_path.find_longest_path

    generate_blocks(cols, rows, checkpoints, route=True, enter=start, exist=end, fpath_finder=path_finder)
    contact_image = contact_blocks(rows, cols)
    print_img(img = contact_image)

if  __name__ ==  '__main__':

    # raw_map_printer()
    route_map_printer(start="06_18", end="14_07")