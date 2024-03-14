import pygame

class Done():
    def __init__(self):
        self.is_selected = False
        self.is_win = 0
        self.rect = pygame.Rect(500, 100, 100, 60)
    
    def set_is_selected(self, value):
        self.is_selected = value

    def contains(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen, font):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(font.render("Done", True, (0, 0, 0)), (500 + 20, 100 + 15))
    
    def set_is_win(self, value):
        self.is_win = value
    
    def draw_result(self, screen, font):
        if self.is_win == 1:
            screen.blit(font.render("YOU WIN!", True, (0, 255, 0)), (500, 200))
        elif self.is_win == 2:
            screen.blit(font.render("YOU LOSE!", True, (255, 0, 0)), (500, 200))
