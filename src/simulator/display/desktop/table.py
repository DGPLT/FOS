import pygame
import json
    
width = 700
height = 600
cell_size = 100
grid_width = 7
grid_height = 10
white = (255, 255, 255)
black = (0, 0, 0)
scroll_x = 0
scroll_y = 0

pygame.init()
screen = pygame.display.set_mode((width, height))
unit_table = #json 파일 주소

with open(unit_table, 'r') as fp:
    unit_data = json.load(fp)
        
unit_grid = [["Ordered", "Available", "ETR", "ETD", "ETA", "Base", "CWL"]]

  #TODO
              
                    
class TableUpdate():

    def table_update():
        screen.fill(black)

        for row in range(grid_height):
            for col in range(grid_width):
                number = unit_grid[row][col]
                x = col * cell_size - scroll_x
                y = row * cell_size - scroll_y
                pygame.draw.rect(screen, white, (x, y, cell_size, cell_size))
                font = pygame.font.Font(None, 32)
                text = font.render(str(number), True, black)
                text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                screen.blit(text, text_rect)
        
        pygame.display.flip()
    
        



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_y -= cell_size
                elif event.button == 5:
                    scroll_y += cell_size
                        
        table_update()
    
    
pygame.quit()
