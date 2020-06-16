import random
import shelve
import pygame

pygame.init()

dis_width = 600
dis_height = 400
display = pygame.display.set_mode((dis_width,dis_height))
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)
started = False
font_style = pygame.font.SysFont("bahnschrift", 25)
score_style = pygame.font.SysFont("Arial",25)
score_s = score_style.render("Score:", True, white)
start_style = pygame.font.SysFont("Impact", 40)

play = start_style.render(('PLAY'), True, white)
play_r = play.get_rect()
play_r.x, play_r.y = dis_width / 3, dis_height / 4
H = False


def high_score_f():
    d = shelve.open("score.txt")
    s = d["score"]
    high_score_s = score_style.render(f"Your high score is: {s}", True, white)
    display.blit(high_score_s, [dis_width/6, dis_height/10])
    d.close()


def our_snake(snake_block,snake_list):
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], snake_block, snake_block])


def score(sc=0):
    point_s = score_style.render(str(sc), True, white)
    display.blit(point_s, [dis_width / 6, dis_height / 15])


def message(msg,color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [dis_width/6, dis_height/3])


def start_img(img):
    display.blit(img,[dis_width/2.5, dis_height/4])


def normall(bool):
    if bool:
        n_s = score_style.render("Normal (current)", True, green)
    else:
        n_s = score_style.render("Normal", True, white)
    display.blit(n_s, [dis_width / 2.5, dis_height / 2.7])
    normal_r = n_s.get_rect()
    normal_r.x,normal_r.y = dis_width / 2.5, dis_height / 2.7
    return normal_r


def hard(bool):
    if bool:
        h_s = score_style.render("Hard (current)", True, green)
    else:
        h_s = score_style.render("Hard", True, white)
    display.blit(h_s,[dis_width/2.5, dis_height/2.2])
    hard_r = h_s.get_rect()
    hard_r.x, hard_r.y = dis_width/2.5, dis_height/2.2
    return hard_r


def gameloop(H):
    x1 = dis_width/2
    y1 = dis_height/2
    sc = 0
    high_score = sc
    x1_new = 0
    y1_new = 0
    speed = 7
    snake_list = []
    length_of_snake = 1

    clock = pygame.time.Clock()
    foodx = round(random.randrange(0,dis_width - 15)//10) * 10.0
    foody = round(random.randrange(0, dis_height - 15) // 10) * 10.0
    pygame.display.update()
    pygame.display.set_caption("The Ugly snake")
    game_over = False
    game_close = False
    while not game_over:
        while game_close:
            d = shelve.open("score.txt")
            try:
                if high_score > d["score"]:
                    d["score"] = high_score
            except KeyError:
                d["score"] = high_score
            d.close()
            display.fill(black)
            high_score_f()
            message("You Lost! Press Q-Quit or P-Play again",red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_p:
                        gameloop(H)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_new = -25
                    y1_new = 0
                elif event.key == pygame.K_RIGHT:
                    x1_new = 25
                    y1_new = 0
                elif event.key == pygame.K_DOWN:
                    y1_new = 25
                    x1_new = 0
                elif event.key == pygame.K_UP:
                    y1_new = -25
                    x1_new = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_new
        y1 += y1_new
        display.fill(black)
        pygame.draw.rect(display,white,[foodx,foody,15,15])
        display.blit(score_s, [dis_width / 20, dis_height / 15])
        score(sc)
        pygame.display.update()
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
        our_snake(15, snake_list)

        pygame.display.update()
        if x1 in range(int(foodx)-15,int(foodx)+15) and y1 in range(int(foody)-15,int(foody)+15):
            sc += 1
            high_score = sc
            score(sc)
            if sc % 5 == 0 and H and sc > 0:
                speed += 1
            pygame.display.update()
            foodx = round(random.randrange(0, dis_width - 15) // 10) * 10
            foody = round(random.randrange(0, dis_height - 15) // 10) * 10
            length_of_snake += 1
            message("We are getting bigger!!", white)
        clock.tick(speed)

    pygame.quit()
    quit()


h = False
n = True

while not started:
    for event in pygame.event.get():
        display.fill(black)
        start_img(play)
        normal_r = normall(n)
        hard_r = hard(h)
        if hard_r.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                h = True
                n = False
                H = True
        elif normal_r.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                h = False
                n = True
                H = False
        elif play_r.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                started = True
                break
    pygame.display.update()
if started:
    gameloop(H)
