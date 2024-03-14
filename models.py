import pygame

class Cell():
    def __init__(self, line_index, block_index, row_index, cell_index, start_value, user_value):
        self.line_index = line_index
        self.block_index = block_index
        self.row_index = row_index
        self.cell_index = cell_index
        self.start_value = start_value
        self.user_value = user_value
        self.is_selected = False
        self.rect = pygame.Rect(100, 100, 40, 40)
    
    def contains(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Line():
    def __init__(self, line_index, block_index, row_index, cells):
        self.line_index = line_index
        self.block_index = block_index
        self.row_index = row_index
        self.cells = cells

class Block():
    def __init__(self, block_index, row_index, lines):
        self.block_index = block_index
        self.row_index = row_index
        self.lines = lines

class Row():
    def __init__(self, row_index, blocks):
        self.row_index = row_index
        self.blocks = blocks