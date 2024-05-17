import pygame as pg

pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
pg.display.set_caption("Pong")
s_width, s_height = screen.get_size()
clock = pg.time.Clock()
running = True

ball_radius = s_width/64
ball_x, ball_y = ((s_width/2), (s_height/2))

paddle_x, paddle_y = (16, (s_height/2)-64)

p_spd, x_spd, y_spd = (4, -4, 4)

p_score = 0

while running:

    for e in pg.event.get():

        if e.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_UP]:
        paddle_y -= p_spd 
    if keys[pg.K_DOWN]:
        paddle_y += p_spd

    screen.fill("white")
    # begin render

    pg.draw.circle(screen, "black", (ball_x, ball_y), ball_radius)
    pg.draw.rect(screen, "black", ((paddle_x, paddle_y), (32, 128)))

    # end render
    pg.display.flip()

    clock.tick(60)

    # check for border collision
    if ball_y < 0 or ball_y > s_height:
        y_spd += int(-y_spd*2)
    if ball_x > s_width:
        x_spd += int(-x_spd*2)
    if ball_x < 0:
        ball_x, ball_y = (int(s_width/2), int(s_height/2))
        paddle_x, paddle_y = (16, int(s_height/2)-64)
        p_score -= 1

    # check for paddle collision
    if (ball_y + y_spd) in range(int(paddle_y), int(paddle_y+128)) and (ball_x+x_spd) in range(int(paddle_x), int(paddle_x+32)):
        y_spd += int(-y_spd*2)
        x_spd += int(-x_spd*2)
        p_score += 1
    else:
        print("none")
    
    ball_y += y_spd 
    ball_x += x_spd

    #if p_score < 0:
        #running = False

pg.quit()
