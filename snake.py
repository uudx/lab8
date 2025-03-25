import pygame
import random

pygame.init()

#constants
w, h = 600, 400
grid = 20
spped_plus = 2  # Speed increase per level
food_count_to_level_up = 3

#xreate window
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

#snake initial state(list of (x, y) positions)
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (grid, 0)

#function to generate food at a random position
def generate_food():
    while True:
        food = (random.randint(0, (w // grid) - 1) * grid,random.randint(0, (h // grid) - 1) * grid)
        #ensure food does not appear on snake
        if food not in snake:  
            return food

food = generate_food()
score = 0
level = 1
speed = 10

running = True
while running:
    #black backround
    screen.fill((0,0,0))
    
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, grid):
                snake_dir = (0, -grid)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -grid):
                snake_dir = (0, grid)
            elif event.key == pygame.K_LEFT and snake_dir != (grid, 0):
                snake_dir = (-grid, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-grid, 0):
                snake_dir = (grid, 0)
    
    #move snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    #check for collisions with walls
    if new_head[0] < 0 or new_head[0] >= w or new_head[1] < 0 or new_head[1] >= h:
        running = False
    
    #check for collisions with itself
    if new_head in snake:
        running = False
    
    snake.insert(0, new_head)
    
    #check if food is eaten
    if new_head == food:
        score += 1
        food = generate_food()
        if score % food_count_to_level_up == 0:
            level += 1
            speed += spped_plus  #increase speed
    else:
        snake.pop()
    
    #draw food
    pygame.draw.rect(screen, (255,0,0), (*food, grid, grid))
    
    #draw snake
    for segment in snake:
        pygame.draw.rect(screen, (0,255,0), (*segment, grid, grid))
    
    #display score and level
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}  Level: {level}", True, (255,255,255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(speed)
pygame.quit()
