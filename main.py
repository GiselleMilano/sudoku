import pygame
import re
from pygame.locals import *
from models import Block, Cell, Line, Row
from widgets import Done

# Make 3 blocks to each board row, each block contains 3 lines and each line contains 9 cells
def make_blocks(board):
    block_0 = []
    block_1 = []
    block_2 = []

    for row in board:
        for index_cell, cell in enumerate(row):
            if index_cell <= 2:
                block_0.append(cell)
            elif index_cell > 2 and index_cell <= 5:
                block_1.append(cell)
            elif index_cell > 5 and index_cell <= 8:
                block_2.append(cell)
    
    new_block_0 = []
    new_block_1 = []
    new_block_2 = []

    for index_block, block in enumerate([block_0, block_1, block_2]):
        line_0 = []
        line_1 = []
        line_2 = []

        for index_cell, cell in enumerate(block):
            if index_cell <= 2:
                line_0.append(cell)
            elif index_cell > 2 and index_cell <= 5:
                line_1.append(cell)
            elif index_cell > 5 and index_cell <= 8:
                line_2.append(cell)

        if (index_block == 0):
            new_block_0.append(line_0)
            new_block_0.append(line_1)
            new_block_0.append(line_2)
        elif (index_block == 1):
            new_block_1.append(line_0)
            new_block_1.append(line_1)
            new_block_1.append(line_2)
        elif (index_block == 2):
            new_block_2.append(line_0)
            new_block_2.append(line_1)
            new_block_2.append(line_2)

    return [new_block_0, new_block_1, new_block_2]

# Put into each row the Models objects instances and blocks
def make_board_row(blocks, row_index):
    new_blocks = []

    for index_block, block_aux in enumerate(blocks):
        lines_obj_for_block = []
        
        for index_line, line_aux in enumerate(block_aux):
            cells_obj_for_line = []
        
            for index_cell, value in enumerate(line_aux):
                cell = Cell(index_line, index_block, row_index, index_cell, value, 0)
                cells_obj_for_line.append(cell)

            line = Line(index_line, index_block, row_index, cells_obj_for_line)
            lines_obj_for_block.append(line)

        block = Block(index_block, row_index, lines_obj_for_block)
        new_blocks.append(block)

    return Row(row_index, new_blocks)

# Divide the basic board in 3 rows and call make_blocks() to fill the board with the Models
def convert_to_board(sample):
    return [make_board_row(make_blocks([sample[0], sample[1], sample[2]]), 0), make_board_row(make_blocks([sample[3], sample[4], sample[5]]), 1), make_board_row(make_blocks([sample[6], sample[7], sample[8]]), 2)]

# All blocks start with the position x = 100
def get_pos_by_block_index(index):
    if index == 0:
        return 100
    elif index == 1:
        return 220
    elif index == 2:
        return 340

# Switch cases for get_pos_by_line_index()
def row_index_0(index):
    if index == 0:
        return 100
    elif index == 1:
        return 140
    elif index == 2:
        return 180

def row_index_1(index):
    if index == 0:
        return 220
    elif index == 1:
        return 260
    elif index == 2:
        return 300

def row_index_2(index):
    if index == 0:
        return 340
    elif index == 1:
        return 380
    elif index == 2:
        return 420

def get_pos_by_line_index(index, row_index):
    switch = {
        0: row_index_0,
        1: row_index_1,
        2: row_index_2
    }
    return switch.get(row_index, lambda: print("Row Index Invalid"))(index)

def draw_board(board, screen, font):
    for row in board:
        for block in row.blocks:
            pos_x_by_block = get_pos_by_block_index(block.block_index)

            for line in block.lines:
                pos_y_by_line = get_pos_by_line_index(line.line_index, row.row_index)
                
                for cell in line.cells:
                    cell.rect.x = pos_x_by_block + (40 * cell.cell_index)
                    cell.rect.y = pos_y_by_line
                    
                    if cell.is_selected:
                        pygame.draw.rect(screen, (252, 192, 210), cell.rect)
                        pygame.draw.rect(screen, (0,0,0), cell.rect, 2)
                    else:
                        pygame.draw.rect(screen, (0,0,0), cell.rect, 2)
                    
                    if cell.user_value != 0:
                        screen.blit(font.render(str(cell.user_value), True, (209, 13, 91)), (cell.rect.x + 12, cell.rect.y + 8))
                    if cell.start_value != 0:
                        screen.blit(font.render(str(cell.start_value), True, (0, 0, 0)), (cell.rect.x + 12, cell.rect.y + 8))

def validate_digit(string):
    patron = r'^[0-9]$'
    return re.match(patron, string)

def get_cells_block(row_index, block_index, board):
    cells = []

    for row in board:
        if row.row_index == row_index:
            for block in row.blocks:
                if block.block_index == block_index:
                    for line in block.lines:
                        for cell in line.cells:
                            cells.append(get_cell_value(cell.start_value, cell.user_value))
    return cells

def get_cells_horizontal(row_index, line_index, board):
    line_cells = []

    for row in board:
        if row.row_index == row_index:
            for block in row.blocks:
                for line in block.lines:
                    if line.line_index == line_index:
                        for cell in line.cells:
                            line_cells.append(get_cell_value(cell.start_value, cell.user_value))
    return line_cells

def get_cells_vertical(block_index, cell_index, board):
    line_cells = []

    for row in board:
        for block in row.blocks:
            if block.block_index == block_index:
                for line in block.lines:
                    for cell in line.cells:
                        if cell.cell_index == cell_index:
                            line_cells.append(get_cell_value(cell.start_value, cell.user_value))
    return line_cells

def is_cell_value_unique(array, value):
    return not (array.count(value) > 1)

def get_final_result(validate_results):
    return all(validate_results)

def get_cell_value(start_value, user_value):
    if start_value == 0:
        return user_value
    return start_value

def validate_board(board):
    validate_results = []

    for row in board:
        for block in row.blocks:
            for line in block.lines:
                for cell in line.cells:
                    cell_value = get_cell_value(cell.start_value, cell.user_value)

                    cells_in_block = get_cells_block(row.row_index, block.block_index, board)
                    cells_in_horizontal = get_cells_horizontal(row.row_index, line.line_index, board)
                    cells_in_vertical = get_cells_vertical(block.block_index, cell.cell_index, board)

                    if (is_cell_value_unique(cells_in_block, cell_value) and is_cell_value_unique(cells_in_horizontal, cell_value) and is_cell_value_unique(cells_in_vertical, cell_value)):
                        validate_results.append(True)
                    else:
                        validate_results.append(False)
    
    return get_final_result(validate_results)

def is_cell_incompleted(board):
    for row in board:
        for block in row.blocks:
            for line in block.lines:
                for cell in line.cells:
                    if get_cell_value(cell.start_value, cell.user_value) == 0:
                        return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.SysFont('Arial', 25)
    new_text_rect = ""
    done = Done()

    sample = [
        [0, 3, 2, 1, 9, 0, 7, 4, 0],
        [4, 0, 9, 5, 0, 6, 8, 0, 2],
        [0, 5, 0, 0, 3, 4, 0, 1, 6],
        [8, 0, 0, 0, 1, 0, 3, 5, 7],
        [3, 0, 0, 8, 0, 5, 4, 0, 9],
        [0, 9, 4, 0, 2, 7, 1, 6, 8],
        [1, 0, 7, 0, 0, 2, 6, 8, 0],
        [0, 6, 0, 7, 8, 0, 5, 0, 4],
        [9, 0, 5, 6, 4, 3, 0, 7, 1],
    ]

    sample_resolved = [
        [6, 3, 2, 1, 9, 8, 7, 4, 5],
        [4, 1, 9, 5, 7, 6, 8, 3, 2],
        [7, 5, 8, 2, 3, 4, 9, 1, 6],
        [8, 2, 6, 4, 1, 9, 3, 5, 7],
        [3, 7, 1, 8, 6, 5, 4, 2, 9],
        [5, 9, 4, 3, 2, 7, 1, 6, 8],
        [1, 4, 7, 9, 5, 2, 6, 8, 3],
        [2, 6, 3, 7, 8, 1, 5, 9, 4],
        [9, 8, 5, 6, 4, 3, 2, 7, 1],
    ]

    board = convert_to_board(sample)
       
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if done.contains(pygame.mouse.get_pos()):
                    done.set_is_selected(done.contains(pygame.mouse.get_pos()))
                    if is_cell_incompleted(board) == False:
                        validate_results = validate_board(board)

                        if validate_results:
                            done.set_is_win(1)
                        else:
                            done.set_is_win(2)

                for row in board:
                    for block in row.blocks:
                        for line in block.lines:
                            for cell in line.cells:
                                cell.is_selected = cell.contains(pygame.mouse.get_pos())
                                new_text_rect = ""
            elif event.type == KEYDOWN:
                for row in board:
                    for block in row.blocks:
                        for line in block.lines:
                            for cell in line.cells:
                                if cell.is_selected:
                                    if validate_digit(event.unicode) and len(new_text_rect) < 1:
                                        if cell.start_value == 0:
                                            new_text_rect += event.unicode
                                            cell.user_value = int(new_text_rect)
        screen.fill((255,255,255))
        draw_board(board, screen, font)
        done.draw(screen, font)
        done.draw_result(screen, font)

        pygame.display.flip()
        clock.tick(60)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()