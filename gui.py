import pygame
from button import Button


class GUI:
    def __init__(self, screen, bg, width, height):
        self.screen = screen
        self.bg = bg
        self.width = width
        self.height = height

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("font.ttf", size)

    def main_menu(self):
        rows = cols = None
        input_rows = pygame.Rect(self.width/4 - 150, 250, 300, 35)
        input_cols = pygame.Rect(self.width - self.width/3 - 25, 250, 300, 35)
        color_inactive_rows = color_inactive_cols = pygame.Color('#03bafc')
        color_active_rows = color_active_cols = pygame.Color('Violet')
        color_rows = color_inactive_rows
        color_cols = color_inactive_cols
        active_rows = active_cols = False
        text_rows = text_cols = ''
        while True:

            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            rows_text = self.get_font(50).render("Rows: ", True, "White")
            rows_rect = rows_text.get_rect(center=(self.width / 4, 175))

            cols_text = self.get_font(50).render("Cols: ", True, "White")
            cols_rect = cols_text.get_rect(center=(self.width - (self.width/4), 175))

            maze_text = self.get_font(90).render("MAZE", True, "#03bafc")
            maze_rect = maze_text.get_rect(center=(self.width/2, 80))

            bfs_button = Button(image=pygame.image.load("Play Rect.png"), pos=(self.width/2, 350),
                                text_input="BFS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="Green")

            dfs_button = Button(image=pygame.image.load("Play Rect.png"), pos=(self.width/2, 500),
                                text_input="DFS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="Green")

            astar_button = Button(image=pygame.image.load("Play Rect.png"), pos=(self.width/2, 650),
                                  text_input="A*", font=self.get_font(75), base_color="#d7fcd4", hovering_color="Green")

            quit_button = Button(image=pygame.image.load("Quit Rect.png"), pos=(self.width/2, 800),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="Red")


            maze_img = pygame.image.load('Play Rect.png')
            rows_img = pygame.image.load('Quit Rect.png')
            cols_img = pygame.image.load('Quit Rect.png')

            self.screen.blit(rows_img, (self.width / 4 - 200, 125))
            self.screen.blit(cols_img, (self.width - self.width / 3 - 50, 125))
            self.screen.blit(maze_img, (self.width/3 + 75, 25))
            self.screen.blit(maze_text, maze_rect)
            self.screen.blit(rows_text, rows_rect)
            self.screen.blit(cols_text, cols_rect)

            for button in [bfs_button, dfs_button, astar_button, quit_button]:
                button.change_color(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rows.collidepoint(event.pos):
                        active_rows = True
                    else:
                        active_rows = False
                    color_rows = color_active_rows if active_rows else color_inactive_rows

                    if input_cols.collidepoint(event.pos):
                        active_cols = True
                    else:
                        active_cols = False
                    color_cols = color_active_cols if active_cols else color_inactive_cols

                if event.type == pygame.KEYDOWN:
                    if active_rows:
                        if event.key == pygame.K_RETURN:
                            rows = int(text_rows)
                            text_rows = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text_rows = text_rows[:-1]
                            if len(text_rows) == 0:
                                rows = None
                        else:
                            text_rows += event.unicode

                    if active_cols:
                        if event.key == pygame.K_RETURN:
                            cols = int(text_cols)
                            text_cols = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text_cols = text_cols[:-1]
                            if len(text_cols) == 0:
                                cols = None
                        else:
                            text_cols += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rows is not None and cols is not None:
                        if bfs_button.check_for_input(mouse_pos):
                            return 'bfs', rows, cols
                        if dfs_button.check_for_input(mouse_pos):
                            return 'dfs', rows, cols
                        if astar_button.check_for_input(mouse_pos):
                            return 'astar', rows, cols
                    if quit_button.check_for_input(mouse_pos):
                        exit()

            font = pygame.font.Font(None, 35)

            text_surface_rows = font.render(text_rows, True, pygame.Color('White'))
            pygame.draw.rect(self.screen, color_rows, input_rows, 2)
            self.screen.blit(text_surface_rows, (input_rows.x + 5, input_rows.y + 5))

            text_surface_cols = font.render(text_cols, True, pygame.Color('White'))
            pygame.draw.rect(self.screen, color_cols, input_cols, 2)
            self.screen.blit(text_surface_cols, (input_cols.x + 5, input_cols.y + 5))

            pygame.display.update()
