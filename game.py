import pygame
from helpers import generate_gradient_arr, shuffle_gradient, identical
from levels import load_specific_level

pygame.init()
WIDTH,HEIGHT = 600,700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Py love Hue')
moves_font = pygame.font.Font('./SupremeSpike-KVO8D.otf', 30)
win_font = pygame.font.Font('./SupremeSpike-KVO8D.otf', 76)
title_font = pygame.font.Font('./SupremeSpike-KVO8D.otf', 52)
next_button_rect = pygame.Rect(0, 0, 200, 60)
a = 0


clock = pygame.time.Clock()
running = True

current_level = 0
level = None
w,h = None,None
tile_size  = None
c_start, c_end = None,None
angle = None

img = None
anchors=None
shuffled_img = None

rects = None
start_x, start_y = None,None

selected = None
selected_idx = -1
solved = False
total_moves = 0

STATE_MENU = "menu"
STATE_GAME = "game"
current_state = STATE_MENU
selected = None
selected_idx = -1
solved = False
total_moves = 0
def initialize_game():
    global level,w,h,tile_size,c_start, c_end, angle, img, shuffled_img, rects, tile_size, start_x, start_y, selected, selected_idx, solved, total_moves, a
    level = load_specific_level(current_level)
    w,h = level['w'], level['h']
    tile_size  = min(WIDTH // w, HEIGHT // h)
    c_start, c_end = level['c_start'], level['c_end']
    angle = level['angle']

    img = generate_gradient_arr(w,h,c_start,c_end, direction='diag',angle=angle)
    anchors=level['anchors']
    shuffled_img = shuffle_gradient(img=img, anchors=anchors)

    rects = []
    start_x, start_y = int((WIDTH - (h*tile_size))/2), int((HEIGHT - (w*tile_size))/2)
    row, col = 0,0
    for i in range(start_x, start_x + h*tile_size, tile_size):
        row = 0
        for j in range(start_y, start_y + w*tile_size, tile_size):
                rects.append((pygame.Rect(i, j, tile_size, tile_size), (row, col), True if (row, col) in anchors else False))
                row+=1
        col += 1
    selected = None
    selected_idx = -1
    solved = False
    total_moves = 0
    a = 0
    # print(rects)
    

initialize_game()
print(len(rects))
def draw_main_menu():
    # 1. Render Title
    title_surf = title_font.render("Py LOVE HUE", True, (0, 0, 0))
    title_rect = title_surf.get_rect(center=(WIDTH//2, 200))
    screen.blit(title_surf, title_rect)

    global play_button_rect
    play_button_rect = pygame.Rect(0, 0, 200, 60)
    play_button_rect.center = (WIDTH//2, WIDTH//2)
    
    pygame.draw.rect(screen, (50, 50, 50), play_button_rect, border_radius=10)
    
    play_text = moves_font.render("PLAY", True, (255, 255, 255))
    text_rect = play_text.get_rect(center=play_button_rect.center)
    screen.blit(play_text, text_rect)


show_shuffled = False
def show_orig_gradient_for_seconds(n):
    global show_shuffled
    while n > 0:
        n -= 0.01
        print(round(n))
    show_shuffled = True
        
        

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos) and current_state == STATE_MENU:
                current_state = STATE_GAME
                show_shuffled = False 
                start_time = pygame.time.get_ticks()
            if next_button_rect.collidepoint(event.pos) and solved:
                current_level += 1
                initialize_game()
                show_shuffled = False 
                start_time = pygame.time.get_ticks()

            elif not solved and show_shuffled:
                for i, rect_data in enumerate(rects):
                    # rect_data[0] is the pygame.Rect, rect_data[1] is the (row, col) index
                    if rect_data[0].collidepoint(event.pos):
                        print("Found!")
                        # 1. Check if the tile is an anchor before selecting!
                        grid_pos = rect_data[1]
                        if rect_data[2]:
                            print('Touched an anchor!')
                            continue # Ignore clicks on anchored tiles

                        if selected_idx == -1:
                            # FIRST CLICK
                            selected_idx = i
                            print(f"Selected tile at {grid_pos}")
                        else:
                            # SECOND CLICK
                            target_idx = i
                            
                            # If player clicks the same tile twice, just deselect
                            if target_idx == selected_idx:
                                print('Selected Same One')
                                selected_idx = -1
                                continue

                            # Get the grid coordinates for both
                            sel_coords = rects[selected_idx][1]
                            tar_coords = rects[target_idx][1]
                            
                            # SWAP COLORS in the image array
                            # Using a temp variable for safety
                            temp_color = shuffled_img[sel_coords[0], sel_coords[1]].copy()
                            shuffled_img[sel_coords[0], sel_coords[1]] = shuffled_img[tar_coords[0], tar_coords[1]]
                            shuffled_img[tar_coords[0], tar_coords[1]] = temp_color

                            # RESET state for next turn
                            selected_idx = -1
                            total_moves += 1
                            if (identical(img, shuffled_img)):
                                solved = True
                                print("Solved!")
                            # BREAK the loop so we don't process more collisions for this one click
                            break



    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    if current_state == STATE_MENU:
        draw_main_menu()
    elif current_state == STATE_GAME:
        current_time = pygame.time.get_ticks()
        if not show_shuffled and current_time - start_time > 3000:
            show_shuffled = True
        # RENDER YOUR GAME HERE
        moves_surface = moves_font.render(f'Moves: {total_moves}', True, (0,0,0))
        screen.blit(moves_surface, (15,15))
        k = 0
        for i in range(h):
            for j in range(w):

                if show_shuffled:
                    pygame.draw.rect(screen, shuffled_img[j,i]*255,rects[k][0])
                    if selected_idx == k:
                        pygame.draw.rect(screen, (255,255,0), rects[k][0], 4)
                else:
                    pygame.draw.rect(screen, img[j,i]*255,rects[k][0])
                if rects[k][2]:
                    pygame.draw.circle(screen, (0,0,0), (rects[k][0].x + (tile_size/2), rects[k][0].y + (tile_size/2)), tile_size/12)
                k+=1
        if current_time - start_time > 0:
            text_surface = None
            if current_time - start_time < 1000:
                text_surface = win_font.render('3', True, (0, 0, 0))
            elif current_time - start_time < 2000:
                text_surface = win_font.render('2', True, (0, 0, 0))
            elif current_time - start_time < 3000:
                text_surface = win_font.render('1', True, (0, 0, 0))

            if text_surface:
                text_rect = text_surface.get_rect()
                screen_center = screen.get_rect().center
                text_rect.center = screen_center
                screen.blit(text_surface, text_rect)
            
        if solved:
            text_surface = win_font.render('You Win!', True, (0, 0, 0))
            text_surface.set_alpha(int(a))
            text_rect = text_surface.get_rect()
            screen_center = screen.get_rect().center
            text_rect.center = screen_center
            a = min(a+2, 255)
            next_button_rect.center = (WIDTH//2, HEIGHT-(HEIGHT//4))
    
            
            next_text = moves_font.render("NEXT", True, (255, 255, 255))
            next_rect = next_text.get_rect(center=next_button_rect.center)
            
            screen.blit(text_surface, text_rect)
            if a >= 255:
                pygame.draw.rect(screen, (50, 50, 50), next_button_rect, border_radius=10)
                screen.blit(next_text, next_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60



pygame.quit()