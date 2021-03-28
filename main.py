import pygame, sys, random

# initialization
pygame.init()
clock = pygame.time.Clock()

# screen setup
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# colors
bg_color = pygame.Color("grey12")
light_grey = (200,200,200)

# ball settings
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))

# setup player
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
player_speed = 0

# setup opponent
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# setup ball
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 -15, 30, 30)

# text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# score timer
score_time = True


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    elif ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.right - opponent.left) > 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def opponent_ai():
    if opponent.top < ball.y:
        opponent.y += 16
    if opponent.bottom > ball.y:
        opponent.y -= 16
    if opponent.y <= 10:
        opponent.y = 10
    elif opponent.bottom >= screen_height - 10:
        opponent.bottom = screen_height - 10


def ball_reset():
    global ball_speed_y, ball_speed_x, score_time

    ball.center = (screen_width/2, screen_height/2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 1000:
        number_three = game_font.render("3", True, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 - 50))
    if 1000 < current_time - score_time < 2000:
        number_two = game_font.render("2", True, light_grey)
        screen.blit(number_two, (screen_width/2 - 10, screen_height/2 - 50))
    if 2000 < current_time - score_time < 3000:
        number_one = game_font.render("1", True, light_grey)
        screen.blit(number_one, (screen_width/2 - 10, screen_height/2 - 50))

    if current_time - score_time < 3000:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1,-1))
        ball_speed_x = 7 * random.choice((1,-1))
        score_time = None

    

def player_animation():
    player.y += player_speed
    if player.y <= 10:
        player.y = 10
    elif player.bottom >= screen_height - 10:
        player.bottom = screen_height - 10

while True:
    # checking for events
    for event in pygame.event.get():
        # checking for close event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed = 10
            if event.key == pygame.K_UP:
                player_speed = -10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed = 0
            if event.key == pygame.K_UP:
                player_speed = 0
        
    ball_animation()
    opponent_ai()
    player_animation()

    # visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    if score_time:
        ball_reset()

    # texts
    player_text = game_font.render(f"{player_score}", True, light_grey)
    screen.blit(player_text, (screen_width/2 + 30, screen_height/2 - 15))
    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)
    screen.blit(opponent_text, (screen_width/2 - 47, screen_height/2 - 15))

    # update display
    pygame.display.flip()
    # update display 60 frames per second
    clock.tick(60)