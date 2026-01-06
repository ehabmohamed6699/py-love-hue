import pygame
from helpers import generate_gradient_arr, shuffle_gradient, identical

pygame.init()
WIDTH,HEIGHT = 600,700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Py love Hue')
moves_font = pygame.font.Font('./SupremeSpike-KVO8D.otf', 30)
win_font = pygame.font.Font('./SupremeSpike-KVO8D.otf', 76)
a = 0


clock = pygame.time.Clock()
running = True

w,h = 6, 4
tile_size  = min(WIDTH // w, HEIGHT // h)
c_start, c_end = (0, 255, 180), (120, 40, 0)
angle = 160

img = generate_gradient_arr(w,h,c_start,c_end, direction='diag',angle=angle)
# anchors=[(0,0),(0,3),(5,0),(5,3)]
# anchors=[(1,1),(1,2),(2,1),(2,2),(3,1),(3,2),(4,1),(4,2)]
anchors=[(0,0),(0,1),(0,2),(0,3),(1,0),(1,3),(2,0),(2,3),(3,0),(3,3),(4,0),(4,3),(5,0),(5,1),(5,2),(5,3)]
# anchors=[(0,0),(2,1)]
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
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if not solved:
                for i, rect_data in enumerate(rects):
                    # rect_data[0] is the pygame.Rect, rect_data[1] is the (row, col) index
                    if rect_data[0].collidepoint(event.pos):
                        
                        # 1. Check if the tile is an anchor before selecting!
                        grid_pos = rect_data[1]
                        if rect_data[2]:
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

    # RENDER YOUR GAME HERE
    moves_surface = moves_font.render(f'Moves: {total_moves}', True, (0,0,0))
    screen.blit(moves_surface, (15,15))
    k = 0
    for i in range(h):
         for j in range(w):
              pygame.draw.rect(screen, shuffled_img[j,i]*255,rects[k][0])
              if selected_idx == k:
                pygame.draw.rect(screen, (255,255,0), rects[k][0], 4)
                  
              if rects[k][2]:
                  pygame.draw.circle(screen, (0,0,0), (rects[k][0].x + (tile_size/2), rects[k][0].y + (tile_size/2)), tile_size/12)
              k+=1
    if solved:
        text_surface = win_font.render('You Win!', True, (0, 0, 0))
        text_surface.set_alpha(int(a))
        text_rect = text_surface.get_rect()
        screen_center = screen.get_rect().center
        text_rect.center = screen_center
        a = min(a+2, 255)
        screen.blit(text_surface, text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()