import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block:
            # Create copy of snake including last index
            body_copy = self.body[:]
            # insert new at 0 and apply direction
            body_copy.insert(0, body_copy[0] + self.direction)
            # Copy whole thing back to body copy
            self.body = body_copy[:]
            # revert flag back to false so that snake doesnt keep extending
            self.new_block = False
        else:
            # Create copy of snake leaving out last index
            body_copy = self.body[:-1]
            # insert new at 0 and apply direction
            body_copy.insert(0, body_copy[0] + self.direction)
            # Copy whole thing back to body copy
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number -1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

# Initialise pygame
pygame.init()
cell_size = 40
cell_number = 20
paused = False
# Set the screen size
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
# New clock object for limiting fps
clock = pygame.time.Clock()
# .convert_alpha() converts image to something pygame works with more easily.
apple = pygame.image.load('Graphics/apple1.png').convert_alpha()
apple = pygame.transform.scale(apple, (cell_size, cell_size))

# Creating an event to update the screen
SCREEN_UPDATE = pygame.USEREVENT
#  Triggering that event to happen every 150ms
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    # Check for quit pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Listening for the screen update during the event loop.
        if event.type == SCREEN_UPDATE and not paused:
            main_game.update()

        # Listen for keys pressed and adjust directions accordingly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)


            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)


            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)


            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE:
                paused = not paused

    # Change color of surface
    screen.fill((175, 215, 70))

    main_game.draw_elements()

    pygame.display.update()
    # Limit fps to 60fps
    clock.tick(60)




