# TODO: Settings

import pygame as pg

pg.init()
pg.font.init()

screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
pg.display.set_caption("Pong")
s_width, s_height = screen.get_size()

clock = pg.time.Clock()
running = True

score_text = pg.font.SysFont('Comic Sans', 36)

p_spd, x_spd, y_spd = (6, -10, 4)
ball_start = ((s_width/2)-(s_width/64), (s_height/2)-(s_width/64))
p1_start = (16, (s_height/2)-64)
p2_start = (s_width-48, (s_height/2)-64)

ball = { 'color':'black', 'x':ball_start[0], 'y':ball_start[1], 'r':s_width/64 }
p1 = { 'name':'Player 1', 'color':'black', 'x': p1_start[0], 'y':p1_start[1], 'w': 32, 'h':128, 'score': 0 }
p2 = { 'name':'Player 2', 'color':'black', 'x': p2_start[0], 'y':p2_start[1], 'w': 32, 'h':128, 'score': 0 }

score_limit = 2
winner = ''

def dis_players(surf, p1, p2):
    pg.draw.rect(surf, p1['color'], ((p1['x'], p1['y']), (p1['w'],p1['h'])))
    pg.draw.rect(surf, p2['color'], ((p2['x'], p2['y']), (p2['w'],p2['h'])))

def dis_score(score_s, win_s):
    screen.blit(score_s, (s_width/2-(score_text.size(score_display)[0]/2) ,16))
    screen.blit(win_s, (s_width/2-(score_text.size(winner)[0]/2), s_height/2))

while running:

    score_display = f"Player 1: {p1['score']}         Player 2: {p2['score']}"

    score_surface = score_text.render(score_display, False, (0,0,0))
    win_surface = score_text.render(winner, False, (0,0,0))

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_UP]:
        p2['y']-= p_spd 
    if keys[pg.K_DOWN]: 
        p2['y'] += p_spd
    if keys[pg.K_w]:
        p1['y'] -= p_spd
    if keys[pg.K_s]:
        p1['y'] += p_spd

    screen.fill("white")
    # begin render

    dis_score(score_surface, win_surface)

    if winner == '':
        pg.draw.line(screen, "grey", (int(s_width/2),0), (int(s_width/2), int(s_height))) 

    pg.draw.circle(screen, ball['color'], (ball['x'], ball['y']), ball['r'])
    dis_players(screen, p1, p2)

    # end render
    pg.display.flip()

    if p1['score'] == score_limit or p2['score'] == score_limit:
        continue
        running = False 

    clock.tick(60)

    # check for border collision
    if ball['y'] < 0 or ball['y'] > s_height:
        y_spd += int(-y_spd*2)
    if ball['x'] < 0:
        ball['x'], ball['y'] = (ball_start[0], ball_start[1])
        p1['x'], p1['y'] = p1_start
        p1['score'] -= 1 if p1['score'] > 0 else 0
        p2['score'] += 1
    if ball['x'] > s_width:
        ball['x'], ball['y'] = (ball_start[0], ball_start[1])
        p2['x'], p2['y'] = p2_start
        p1['score'] += 1
        p2['score'] -= 1 if p2['score'] > 0 else 0

    # check for paddle collision
    if (ball['y'] + y_spd) in range(int(p1['y']), int(p1['y']+128)) and (ball['x']+x_spd) in range(int(p1['x']), int(p1['x']+32)):
        x_spd += -int(x_spd*2)
    if (ball['y'] + y_spd) in range(int(p2['y']), int(p2['y']+128)) and (ball['x']+x_spd) in range(int(p2['x']), int(p2['x']+32)):
        x_spd += -int(x_spd*2)
        
    ball['y'] += y_spd 
    ball['x'] += x_spd

    if p1['score'] == score_limit:
        winner = f"{p1['name']} Won with {p1['score']}!"
    if p2['score'] == score_limit:
        winner = f"{p2['name']} Won with {p2['score']}!"
