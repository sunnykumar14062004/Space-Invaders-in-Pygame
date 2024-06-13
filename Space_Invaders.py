import pygame
import random

pygame.init()
clock = pygame.time.Clock()
screen_width = 400
screen_height = 550
border = 5
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.mixer.music.load("Game Music.wav")
pygame.mixer.music.play(-1)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Logo.png")
pygame.display.set_icon(icon)

background_image = pygame.image.load("Background.png")
game_over_image = pygame.image.load("Game Over.png")
plane = pygame.image.load("Plane.png")
enemy = pygame.image.load("Enemy.png")
bullet = pygame.image.load("Bullet.png")

def random_integers():
    minimum_distance = 50
    upper_limit = screen_width - border - 32
    int_1 = random.randint(border, upper_limit)
    int_2 = random.randint(border, upper_limit)
    while abs(int_2 - int_1) < minimum_distance:
        int_2 = random.randint(border, upper_limit)
    return [int_1, int_2]

random_coordinates = random_integers()
enemy_x = [random_coordinates[0], random_coordinates[1]]
enemy_y = [-12, -42]
enemy_y_change = 0.6
enemy_rest_x = -50
enemy_rest_y = 600

bullet_x = []
bullet_y = []
bullet_y_change = -0.6
bullet_rest_x = 500
bullet_rest_y = -50
bullet_time_previous = 0

plane_x = (screen_width - 64) / 2
plane_y = screen_height - 64 - border
plane_x_change = 0
plane_y_change = 0
plane_speed = 0.5

font_score_play = pygame.font.SysFont("Bell MT", 30)
font_score_over = pygame.font.SysFont("Arial Rounded MT Bold", 70)
font_title = pygame.font.SysFont("Times New Roman", 60)
font_credit = pygame.font.SysFont("Times New Roman", 35)
font_button = pygame.font.SysFont("Comic Sans MS", 50)

white = (255, 255, 255)
blue = (106, 90, 205)
yellow = (255, 255, 0)
green = (0, 255, 0)
black = (0, 0, 0)

running = True
state = ""
score_value = 0

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            if state == "":
                if 150 < mouse[0] < 240 and 430 < mouse[1] < 485:
                    state = "play"
                    start = pygame.time.get_ticks()

            if state == "over":

                if 130 < mouse[0] < 235 and 440 < mouse[1] < 490:
                    running = False
                    
                if 105 < mouse[0] < 285 and 340 < mouse[1] < 385:
                    state = "play"
                    start = pygame.time.get_ticks()
                    bullet_time_previous = 0
                    score_value = 0
                    plane_x = (screen_width - 64) / 2
                    plane_y = screen_height - 64 - border

        if event.type == pygame.KEYDOWN:

            if state == "play":

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    plane_x_change = -plane_speed
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    plane_x_change = plane_speed
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    plane_y_change = -plane_speed
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    plane_y_change = plane_speed

                if event.key == pygame.K_SPACE:
                    bullet_time_now = pygame.time.get_ticks()
                    if (bullet_time_now - bullet_time_previous) / 1000 > 0.5:
                        bullet_sound = pygame.mixer.Sound("Bullet.wav")
                        bullet_sound.play()                    
                        bullet_x.append(plane_x + 20)
                        bullet_y.append(plane_y - 18)
                        bullet_time_previous = bullet_time_now

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                plane_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                plane_y_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                plane_x_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                plane_y_change = 0

    if state == "play":
        end = pygame.time.get_ticks()
        screen.blit(background_image, (0, 0))
        
        if int((end - start) / 1000) == 1:
            random_coordinates = random_integers()
            enemy_x.append(random_coordinates[0])
            enemy_x.append(random_coordinates[1])
            enemy_y.append(-12)
            enemy_y.append(-42)
            start = end

        plane_x += plane_x_change
        if plane_x < border:
            plane_x = border
        elif plane_x > screen_width - border - 64:
            plane_x = screen_width - border - 64

        plane_y += plane_y_change
        if plane_y < 50:
            plane_y = 50
        elif plane_y > screen_height - border - 64:
            plane_y = screen_height - border - 64

        plane_rect = plane.get_rect(topleft = (plane_x, plane_y))
        screen.blit(plane, (plane_x, plane_y))

        for i in range(len(bullet_x)):
            screen.blit(bullet, (bullet_x[i], bullet_y[i]))
            bullet_y[i] += bullet_y_change
            if bullet_y[i] < bullet_rest_y:
                bullet_x[i] = bullet_rest_x
                bullet_y[i] = bullet_rest_y

        while True:
            try:
                bullet_x.remove(bullet_rest_x)
                bullet_y.remove(bullet_rest_y)
            except ValueError:
                break

        for i in range(len(enemy_x)):
            enemy_rect = enemy.get_rect(topleft = (enemy_x[i], enemy_y[i]))
            screen.blit(enemy, (enemy_x[i], enemy_y[i]))
            enemy_y[i] += enemy_y_change
            if enemy_y[i] > enemy_rest_y:
                enemy_x[i] = enemy_rest_x
                enemy_y[i] = enemy_rest_y

            if enemy_rect.colliderect(plane_rect):
                state = "over"
                game_over_sound = pygame.mixer.Sound("Game Over.wav")
                game_over_sound.play()
                screen.blit(game_over_image, (0, 0))

                for j in range(len(bullet_y)):
                    bullet_x[j] = bullet_rest_x
                    bullet_y[j] = bullet_rest_y
                for j in range(len(enemy_y)):
                    enemy_x[j] = enemy_rest_x
                    enemy_y[j] = enemy_rest_y
                plane_y *= -1

            for j in range(len(bullet_x)):
                bullet_rect = bullet.get_rect(topleft = (bullet_x[j], bullet_y[j]))
                if enemy_rect.colliderect(bullet_rect):
                    enemy_down_sound = pygame.mixer.Sound("Enemy Down.wav")
                    enemy_down_sound.play()

                    bullet_x[j] = bullet_rest_x
                    bullet_y[j] = bullet_rest_y
                    enemy_x[i] = enemy_rest_x
                    enemy_y[i] = enemy_rest_y
                    score_value += 1

        while True:
            try:
                enemy_x.remove(enemy_rest_x)
                enemy_y.remove(enemy_rest_y)
            except ValueError:
                break
    
    if state == "":
        mouse = pygame.mouse.get_pos()

        game_title = font_title.render("Space  Invaders", True, blue)
        name = font_credit.render("Made By : Sunny Kumar", True, yellow)
        branch = font_credit.render("BE  CSE", True, yellow)
        year = font_credit.render("2021 - 2025", True, yellow)

        if 150 < mouse[0] < 240 and 430 < mouse[1] < 485:
            play = font_button.render("Play", True, green)
        else:
            play = font_button.render("Play", True, white)

        screen.blit(game_title, (10, 30))
        screen.blit(name, (20, 200))
        screen.blit(branch, (180, 250))
        screen.blit(year, (180, 300))
        screen.blit(play, (150, 425))

    if state == "play":
        score = font_score_play.render("Score : " + str(score_value), True, blue)
        screen.blit(score, (10, 10))

    elif state == "over":
        mouse = pygame.mouse.get_pos()

        if 105 < mouse[0] < 285 and 340 < mouse[1] < 385:
            restart = font_button.render("Restart", True, green)
        else:
            restart = font_button.render("Restart", True, blue)
        if 130 < mouse[0] < 235 and 440 < mouse[1] < 490:
            quit = font_button.render("Quit", True, green)
        else:
            quit = font_button.render("Quit", True, blue)
        
        score = font_score_over.render("Score : " + str(score_value), True, black)
        screen.blit(score, (75, 225))
        screen.blit(restart, (105, 325))
        screen.blit(quit, (130, 425))

    clock.tick(240)
    pygame.display.update()