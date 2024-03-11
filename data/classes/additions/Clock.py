import pygame


class Clock:
    def __init__(self, x, y, width, height, color, font_color, initial_time):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font_color = font_color
        self.font = pygame.font.SysFont(None, 36)
        self.initial_time = initial_time
        self.start_time = pygame.time.get_ticks()
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = pygame.time.get_ticks()
            self.running = True

    def stop(self):
        if self.running:
            self.initial_time -= pygame.time.get_ticks() - self.start_time
            self.running = False

    def update(self):
        if self.running:
            self.initial_time -= pygame.time.get_ticks() - self.start_time
            self.start_time = pygame.time.get_ticks()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.get_time_string(), True, self.font_color)
        screen.blit(text_surface, (self.x + 10, self.y + 10))

    def get_time_string(self):
        time_left = max(self.initial_time, 0)  # Ensure time doesn't go negative
        seconds = time_left // 1000
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02}:{seconds:02}"
