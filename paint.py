import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
    
#some constants  
radius = 15
mode = 'blue'
drawing_color = (0, 0, 255)  # Start with blue
background_color = (0, 0, 0)
    
#tools
current_tool = 'pen'  # 'pen', 'rectangle', 'circle', 'eraser'
start_pos = None
points = []
    
#store drawings
drawings = []

def drawLineBetween(screen, index, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

    
while True:
    pressed = pygame.key.get_pressed()
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                screen.fill(background_color)
                drawings = []
                
            #tool selection
            if event.key == pygame.K_p:
                current_tool = 'pen'
            elif event.key == pygame.K_r:
                current_tool = 'rectangle'
            elif event.key == pygame.K_c:
                current_tool = 'circle'
            elif event.key == pygame.K_e:
                current_tool = 'eraser'
                
            #color selection
            if event.key == pygame.K_1:
                drawing_color = (255, 0, 0) 
            elif event.key == pygame.K_2:
                drawing_color = (0, 255, 0) 
            elif event.key == pygame.K_3:
                drawing_color = (0, 0, 255) 
            elif event.key == pygame.K_4:
                drawing_color = (255, 255, 0) 
            elif event.key == pygame.K_5:
                drawing_color = (255, 0, 255)
            elif event.key == pygame.K_6:
                drawing_color = (0, 255, 255) 
            elif event.key == pygame.K_7:
                drawing_color = (255, 255, 255)  
            elif event.key == pygame.K_0:
                drawing_color = (0, 0, 0) 
                
            #radius control
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                radius = min(200, radius + 1)
            elif event.key == pygame.K_MINUS:
                radius = max(1, radius - 1)
            
        #mouse handling for different tools
        if current_tool == 'pen':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #left click
                    points = [event.pos]
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  #left mouse button pressed
                    points.append(event.pos)
                    points = points[-256:]  #limit points
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and points:
                    drawings.append(('pen', points.copy(), radius, drawing_color))
                    points = []
            
        elif current_tool in ['rectangle', 'circle']:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #left click
                    start_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    end_pos = event.pos
                    if current_tool == 'rectangle':
                        drawings.append(('rectangle', start_pos, end_pos, radius, drawing_color))
                    elif current_tool == 'circle':
                        drawings.append(('circle', start_pos, end_pos, radius, drawing_color))
                    start_pos = None
            
        elif current_tool == 'eraser':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #left click
                    points = [event.pos]
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  #left mouse button pressed
                    points.append(event.pos)
                    points = points[-256:]  #limit points
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and points:
                    drawings.append(('pen', points.copy(), radius, background_color))
                    points = []
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  #scroll up
                radius = min(200, radius + 1)
            elif event.button == 5:  #scroll down
                radius = max(1, radius - 1)
        
    screen.fill(background_color)
        
    #draw all saved drawings
    for drawing in drawings:
        if drawing[0] == 'pen':
            _, points, width, color = drawing
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], width, color)
                i += 1
        elif drawing[0] == 'rectangle':
            _, start, end, width, color = drawing
            rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
            pygame.draw.rect(screen, color, rect, width)
        elif drawing[0] == 'circle':
            _, start, end, width, color = drawing
            center = start
            radius_circle = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
            pygame.draw.circle(screen, color, center, radius_circle, width)
        
    #draw current temporary drawing (for rectangle/circle preview)
    if start_pos and current_tool == 'rectangle':
        current_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(start_pos, (current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]))
        pygame.draw.rect(screen, drawing_color, rect, radius)
    elif start_pos and current_tool == 'circle':
        current_pos = pygame.mouse.get_pos()
        radius_circle = int(((current_pos[0] - start_pos[0])**2 + (current_pos[1] - start_pos[1])**2)**0.5)
        pygame.draw.circle(screen, drawing_color, start_pos, radius_circle, radius)
        
    #draw current pen/eraser points
    if points and current_tool in ['pen', 'eraser']:
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, drawing_color if current_tool == 'pen' else background_color)
            i += 1
        
    #display help text
    font = pygame.font.SysFont(None, 24)
    help_text = [
        f"Tool: {current_tool} (P=Pen, R=Rectangle, C=Circle, E=Eraser)",
        f"Color: {drawing_color} (1-7: colors, 0=black)",
        f"Size: {radius} (+/- to change, mouse wheel)"
    ]
    for i, text in enumerate(help_text):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + i * 25))
        
    pygame.display.flip()
    clock.tick(60)
