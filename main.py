import pygame
import time
from ball import Ball
from player_1 import Player_1
from player_2 import Player_2

# set up pygame modules
pygame.init()
pygame.font.init()
intro_font = pygame.font.SysFont('Comic Sans', 60)
title_font = pygame.font.SysFont('Impact', 120)
text_font = pygame.font.SysFont('Arial', 30)
timer_font = pygame.font.SysFont('Arial', 15)
score_font = pygame.font.SysFont('Arial', 15)
pygame.display.set_caption("Kick!")

# set up variables for the display
screen_height = 1000
screen_width = 1661
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

bg = pygame.image.load("map.png")
p1 = Player_1(75, 475)
p2 = Player_2(1500, 475)

# render the text for later
BALL_RADIUS = 10
ball_image_path = "ball.png"  # Path to your ball image file
b = Ball(1661 // 2 - 5, 1000 // 2, BALL_RADIUS, ball_image_path)

pygame.mixer.init()
game_start_sound = pygame.mixer.Sound("game_start.wav")
hooray_sound = pygame.mixer.Sound("hooray.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
game_over_voice = pygame.mixer.Sound("game_over_2.wav")

TARGET_REGION_X = 50
TARGET_REGION_Y = 450
TARGET_REGION_WIDTH = 35
TARGET_REGION_HEIGHT = 100

TARGET_REGION_X_2 = 1555
TARGET_REGION_Y_2 = 450
TARGET_REGION_WIDTH_2 = 35
TARGET_REGION_HEIGHT_2 = 100

def check_if_ball_in_target(ball):
    if (
            TARGET_REGION_X < ball.x < TARGET_REGION_X + TARGET_REGION_WIDTH and TARGET_REGION_Y < ball.y < TARGET_REGION_Y + TARGET_REGION_HEIGHT):
        return True
    return False

def check_if_ball_in_target_2(ball):
    if (
            TARGET_REGION_X_2 < ball.x < TARGET_REGION_X_2 + TARGET_REGION_WIDTH_2 and TARGET_REGION_Y_2 < ball.y < TARGET_REGION_Y_2 + TARGET_REGION_HEIGHT_2):
        return True
    return False

display_intro = title_font.render("Welcome to Kick!", True, (120, 81, 169))
display_intro2 = intro_font.render("Score goals against your opponent to win!", True, (0, 0, 0))
display_intro3 = intro_font.render("WASD for Player 1. Arrow Keys for Player 2.", True, (0, 0, 0))
display_intro4 = text_font.render("Click the button to start.", True, (99, 99, 99))

button_text = text_font.render("Start Game", True, (255, 255, 255))
button_color = (0, 128, 0)
button_rect = pygame.Rect(700, 800, 300, 50)  # Define the button rectangle

p1_score = 0
p2_score = 0
goal = title_font.render("GOOOOOOOAL!", True, (120, 81, 169))
big_score = title_font.render("Player 1 " + str(p1_score) + " - " + str(p2_score) + " Player 2", True, (120, 81, 169))

display_end = title_font.render("Game Over!", True, (255, 0, 0))
display_p1_win = title_font.render("Player 1 Wins!", True, (255, 0, 0))
display_p2_win = title_font.render("Player 2 Wins!", True, (0, 0, 255))
display_tie = title_font.render("It's a tie!", True, (99, 99, 99))

start_time = time.time() + 1
seconds = time.time()
display_string = "Timer: " + str(seconds) + "s"
display_seconds = timer_font.render(display_string, True, (255, 255, 255))
display_score = score_font.render("P1 " + str(p1_score) + " : " + str(p2_score) + " P2", True, (255, 255, 255))

# loop
run = True
game_start = False
game_over = False
collision = False
movement_stopped = False
score_counted_p1 = False
score_counted_p2 = False
counter = 0
goal_display_timer = 60

def reset_game():
    global p1, p2, b, p1_score, p2_score, game_start, game_over, movement_stopped, score_counted_p1, score_counted_p2, start_time, counter, goal_display_timer
    p1 = Player_1(75, 475)
    p2 = Player_2(1500, 475)
    b = Ball(1661 // 2 - 5, 1000 // 2, BALL_RADIUS, ball_image_path)
    p1_score = 0
    p2_score = 0
    game_start = False
    game_over = False
    movement_stopped = False
    score_counted_p1 = False
    score_counted_p2 = False
    counter = 0
    goal_display_timer = 60
    start_time = time.time() + 120

# -------- Main Program Loop -----------
while run:
    if not game_over and game_start:
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_d]:
            p1.move_direction("right")
        if keys[pygame.K_a]:
            p1.move_direction("left")
        if keys[pygame.K_w]:
            p1.move_direction("up")
        if keys[pygame.K_s]:
            p1.move_direction("down")

        if keys[pygame.K_RIGHT]:
            p2.move_direction("right")
        if keys[pygame.K_LEFT]:
            p2.move_direction("left")
        if keys[pygame.K_UP]:
            p2.move_direction("up")
        if keys[pygame.K_DOWN]:
            p2.move_direction("down")

        p1.detect_collision(b)
        p2.detect_collision(b)

        b.move()
        b.update_velocity()

        b.check_collision_with_walls(725, 363)

    if check_if_ball_in_target_2(b):
        if not score_counted_p1:  # Check if the score for Player 1 has not been counted yet
            score_counted_p1 = True  # Set the flag to prevent further incrementing
            score_counted_p2 = False  # Ensure Player 2's flag is reset
            p1_score += 1
            big_score = title_font.render("Player 1  " + str(p1_score) + " - " + str(p2_score) + "  Player 2", True,
                                          (120, 81, 169))  # Update big_score
        b.stop()
        p1.delta = 0
        p2.delta = 0
        movement_stopped = True
    elif check_if_ball_in_target(b):
        if not score_counted_p2:  # Check if the score for Player 2 has not been counted yet
            score_counted_p2 = True  # Set the flag to prevent further incrementing
            score_counted_p1 = False  # Ensure Player 1's flag is reset
            p2_score += 1
            big_score = title_font.render("Player 1  " + str(p1_score) + " - " + str(p2_score) + "  Player 2", True,
                                          (120, 81, 169))  # Update big_score
        b.stop()
        p1.delta = 0
        p2.delta = 0
        movement_stopped = True

    # Update the score display
    display_score = score_font.render("P1 " + str(p1_score) + " : " + str(p2_score) + " P2", True, (255, 255, 255))

    if not game_over and game_start:
        current_time = time.time()
        seconds = round(start_time - current_time, 2)
        display_string = "Timer: " + str(seconds) + "s"
        display_seconds = timer_font.render(display_string, True, (255, 255, 255))
        if seconds <= 0:
            game_over = True
            game_start = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            run = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not game_start:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):  # Check if click is within button
                game_start = True
                game_start_sound.play()
                counter += 1
                if counter == 1:
                    start_time = time.time() + 120
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                reset_game()

    if not game_start or not game_over:
        screen.fill((255, 255, 255))
        screen.blit(display_intro, (400, 250))
        screen.blit(display_intro2, (275, 400))
        screen.blit(display_intro3, (225, 475))
        screen.blit(display_intro4, (700, 700))
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, (button_rect.x + 75, button_rect.y + 10))
    if game_start and not game_over:
        screen.blit(bg, (0, 0))
        b.draw(screen)
        screen.blit(p1.image, p1.rect)
        screen.blit(p2.image, p2.rect)
        screen.blit(display_seconds, (1565, 25))
        screen.blit(display_score, (1565, 40))
        if movement_stopped:
            if goal_display_timer > 0:
                hooray_sound.play()
                screen.fill((255, 255, 255))
                screen.blit(goal, (500, 250))
                screen.blit(big_score, (300, 400))
                goal_display_timer -= 1
            else:
                # Reset flags, restart movement, etc.
                score_counted_p1 = False
                score_counted_p2 = False
                movement_stopped = False
                p1 = Player_1(75, 475)
                p2 = Player_2(1500, 475)
                b = Ball(1661 // 2 - 5, 1000 // 2, BALL_RADIUS, ball_image_path)
                goal_display_timer = 60

    if not game_start and game_over:
        game_over_sound.play()
        game_over_voice.play()
        screen.fill((255, 255, 255))
        screen.blit(display_end, (600, 300))
        big_score = title_font.render("Player 1   " + str(p1_score) + " - " + str(p2_score) + "   Player 2", True,
                                      (120, 81, 169))  # Update big_score
        screen.blit(big_score, (325, 425))  # Use updated big_score
        if p1_score > p2_score:
            screen.blit(display_p1_win, (575, 550))
        if p1_score < p2_score:
            screen.blit(display_p2_win, (575, 550))  # Correct display_p2_win
        if p1_score == p2_score:
            screen.blit(display_tie, (675, 550))
        display_restart = text_font.render("Press Space to Restart", True, (0, 0, 0))
        screen.blit(display_restart, (750, 800))  # Add message to restart game

    pygame.display.update()


pygame.quit()
