import pygame, sys, random
from pygame.math import Vector2


def load_resize_sprite(name):
    path = f'extracted_sprites/{name}'
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (cell_size, cell_size))

def get_random_number():
    return random.randint(1, 10)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = load_resize_sprite('head_up.png')
        self.head_down = load_resize_sprite('head_down.png')
        self.head_right = load_resize_sprite('head_right.png')
        self.head_left = load_resize_sprite('head_left.png')

        self.tail_up = load_resize_sprite('tail_up.png')
        self.tail_down = load_resize_sprite('tail_down.png')
        self.tail_right = load_resize_sprite('tail_right.png')
        self.tail_left = load_resize_sprite('tail_left.png')

        self.body_vertical = load_resize_sprite('body_vertical.png')
        self.body_horizontal = load_resize_sprite('body_horizontal.png')

        self.body_tr = load_resize_sprite('tr.png')
        self.body_tl = load_resize_sprite('tl.png')
        self.body_bl = load_resize_sprite('bl.png')
        self.body_br = load_resize_sprite('br.png')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index -1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_br, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_tl, block_rect)


    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if   tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if   head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down


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

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self, answer):
        self.pos = pygame.math.Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        self.answer = answer
        self.randomize()

    def draw_fruit(self):
        game_font_small = pygame.font.Font(None, 25)
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        screen.blit(apple, fruit_rect)
        number_surface = game_font_small.render(str(self.answer), True, (255, 255, 255))
        number_rect = number_surface.get_rect(center=fruit_rect.center)
        number_rect.y += 5
        screen.blit(number_surface, number_rect)



    def randomize(self):
        self.x = random.randint(0, cell_number -1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y)

class QUESTIONS:
    def __init__(self):
        self.new_question()

    def new_question(self):
        self.a = get_random_number()
        self.b = get_random_number()
        self.text = f"{self.a} + {self.b} = ?"
        self.answer = self.a + self.b

    def draw_question(self):
        question_surface = game_font.render(self.text, True, (255, 255, 255))
        question_x = window_width - 260
        question_y = 850
        question_rect = question_surface.get_rect(center=(question_x, question_y))
        bg_rect = pygame.Rect(question_rect.left - 10, question_rect.top - 5, question_rect.width + 20,
                              question_rect.height + 10)
        pygame.draw.rect(window, (0, 0, 0), bg_rect)
        pygame.draw.rect(window, (255, 255, 255), bg_rect, 2)
        window.blit(question_surface, question_rect)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.question = QUESTIONS()
        self.correct_fruit = FRUIT(self.question.answer)

        wrong_answer = self.question.answer
        while wrong_answer == self.question.answer:
            wrong_answer = random.randint(2, 20)
        self.bad_fruit = FRUIT(wrong_answer)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.correct_fruit.draw_fruit()
        self.bad_fruit.draw_fruit()
        self.draw_score()
        self.question.draw_question()

    def check_collision(self):
        if self.correct_fruit.pos == self.snake.body[0]:
            self.correct_fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.correct_fruit.pos:
                self.correct_fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (155, 195, 50)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                            grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                            pygame.draw.rect(screen, grass_color, grass_rect)
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (255,255,255))
        score_x = window_width - 60
        score_y = 850
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + apple_rect.width, apple_rect.height)

        pygame.draw.rect(window, (0,0,0), bg_rect)
        pygame.draw.rect(window, (255,255,255), bg_rect, 2)
        # screen.blit(score_surface, score_rect)
        window.blit(apple, apple_rect)
        window.blit(score_surface, score_rect)




# Initialise pygame
pygame.init()
cell_size = 40
cell_number = 20
paused = False

#  Set the window size (900 * 800
window_width, window_height = 800, 900
window = pygame.display.set_mode((window_width, window_height))
# Set the screen size (this would be: 800 * 800)
screen = pygame.Surface((cell_size * cell_number, cell_size * cell_number))


# New clock object for limiting fps
clock = pygame.time.Clock()
# .convert_alpha() converts image to something pygame works with more easily.
apple = pygame.image.load('Graphics/apple1.png').convert_alpha()
apple = pygame.transform.scale(apple, (cell_size, cell_size))
# Can add font by importing a ttf file instead of None, it is as a string
game_font = pygame.font.Font(None, 32)


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


    window.fill((30,30,30))
    window.blit(screen, (0,0))
    # Change color of surface
    screen.fill((175, 215, 70))

    main_game.draw_elements()

    pygame.display.update()
    # Limit fps to 60fps
    clock.tick(60)

