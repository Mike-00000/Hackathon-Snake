import pygame
import random

pygame.init()

width = 800
height = 600
background_color = (166, 191, 185)
snake_color = (255, 235, 84)
food_color = (255, 84, 127)
block_size = 40 

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game") 
window.fill(background_color)  

pygame.mixer.music.load("retro-funk.wav")
pygame.mixer.music.set_volume(0.7)  

eat_sound = pygame.mixer.Sound("success-1.wav")
eat_sound.set_volume(0.2)  

class Snake:
    def __init__(self):
        self.x = 0  
        self.y = 0 
        self.direction = "right" 
        self.length = 3 
        self.body = [(self.x, self.y)] 

    def move(self):
        if self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "right":
            self.x += 1

        self.body.insert(0, (self.x, self.y))

        if len(self.body) > self.length:
            self.body.pop()

    def change_direction(self, new_direction):
        if new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction
        elif new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, snake_color, (segment[0] * block_size, segment[1] * block_size, block_size, block_size))

    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head == segment:
                return True
        return False

    @property
    def head_x(self):
        return self.body[0][0]

    @property
    def head_y(self):
        return self.body[0][1]

class Food:
    def __init__(self):
        self.x = random.randint(0, width // block_size - 1)  
        self.y = random.randint(0, height // block_size - 1)  

    def draw(self, surface):
        pygame.draw.rect(surface, food_color, (self.x * block_size, self.y * block_size, block_size, block_size))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.score_rate = 1
        self.clock = pygame.time.Clock()
        self.time_since_last_score_increase = 0

    def run(self):
        pygame.mixer.music.play(-1)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction("up")
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("down")
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("left")
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("right")

            self.snake.move()

            if self.snake.check_self_collision() or self.snake.head_x < 0 or self.snake.head_x >= width // block_size or self.snake.head_y < 0 or self.snake.head_y >= height // block_size:
                running = False
                self.display_final_score()

            if self.check_collision():
                self.snake.length += 1
                self.score += 10
                self.food = Food()
                eat_sound.play() 

            self.time_since_last_score_increase += self.clock.tick(10)
            if self.time_since_last_score_increase >= 1000:
                self.score += self.score_rate
                self.time_since_last_score_increase = 0

            window.fill(background_color)
            self.snake.draw(window)
            self.food.draw(window)
            self.display_score()
            pygame.display.update()

            self.clock.tick(70)

        game_over_sound.play()
        pygame.mixer.music.stop()
        pygame.quit()

    def check_collision(self):
        if self.snake.head_x == self.food.x and self.snake.head_y == self.food.y:
            return True
        return False

    def display_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        window.blit(text, (10, 10))

    def increase_score_rate(self, rate):
        self.score_rate = rate

    def display_final_score(self):
        font = pygame.font.Font(None, 48)
        text = font.render("Final Score: " + str(self.score), True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        window.blit(text, text_rect)
        pygame.display.update()

        pygame.time.delay(2000)

game = Game()
game.increase_score_rate(1)
game_over_sound = pygame.mixer.Sound("braam.wav")
game.run()
