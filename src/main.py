# TODO: Settings
from random import randint as ri
import pygame as pg

pg.init()
pg.font.init()

screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
pg.display.set_caption("Pong")
s_width, s_height = screen.get_size()

clock = pg.time.Clock()
running = True

# Music
pg.mixer.music.load("my_pong_song.wav")

# Settings here down
settings = {'font': 'Comic Sans',
            'font-size': 36,
            'font-color': 'black',
            'paddle-speed': 6,
            'hor-ball-speed': -10,
            'ver-ball-speed': 4,
            'background-color': 'white',
            '1st-player-name': 'Player 1',
            '2nd-player-name': 'Player 2',
            '1st-player-color': 'black',
            '2nd-player-color': 'black',
            'ball-color': 'black',
            'max-score': 5,
            'net': True}

score_text = pg.font.SysFont('Comic Sans', 36)

p_spd, x_spd, y_spd = (settings.get(key) for key in ['paddle-speed', 'hor-ball-speed', 'ver-ball-speed'])
ball_start = (s_width/2, (s_height/2)-(s_width/32))
p1_start = (16, (s_height/2)-64)
p2_start = (s_width-48, (s_height/2)-64)

court = { 'color':settings['background-color'], }
ball = { 'color':settings['ball-color'], 'x':ball_start[0], 'y':ball_start[1], 'r':s_width/64 }
p1 = { 'name':settings['1st-player-name'], 'color':settings['1st-player-color'], 'x': p1_start[0], 'y':p1_start[1], 'w': 32, 'h':128, 'score': 0 }
p2 = { 'name':settings['2nd-player-name'], 'color':settings['2nd-player-color'], 'x': p2_start[0], 'y':p2_start[1], 'w': 32, 'h':128, 'score': 0 }
score_limit = settings['max-score']
winner = ''
new_game = True

def ball_reset():
    ball['x'], ball['y'] = ball_start
    x_spd, y_spd = (0,0)

def dis_entities(surf, ball, p1, p2):
    pg.draw.circle(screen, ball['color'], (ball['x'], ball['y']), ball['r'])
    pg.draw.rect(surf, p1['color'], ((p1['x'], p1['y']), (p1['w'],p1['h'])))
    pg.draw.rect(surf, p2['color'], ((p2['x'], p2['y']), (p2['w'],p2['h'])))

def dis_score(score_d, score_s, win_s):
    screen.blit(score_s, (s_width/2-(score_text.size(score_d)[0]/2) ,16))
    screen.blit(win_s, (s_width/2-(score_text.size(winner)[0]/2), s_height/2))

def court_display(scrn):
    if not new_game:
        score_display = f"Player 1: {p1['score']}         Player 2: {p2['score']}"

        score_surface = score_text.render(score_display, False, (0,0,0))
        win_surface = score_text.render(winner, False, (0,0,0))

    screen.fill(court['color'])
    # begin render

    if not new_game:
        dis_score(score_display, score_surface, win_surface)

        if settings['net']:
            pg.draw.line(scrn, "grey", (int(s_width/2),0), (int(s_width/2), int(s_height))) 

        dis_entities(screen,ball, p1, p2)

    # end render
    pg.display.flip()

def game_over(scrn):
    pass

pg.mixer.music.play(-1)

while running:
    if new_game:
        p1['score'], p2['score'] = (0,0)
        p1['x'],p1['y'] = p1_start
        p2['x'],p2['y'] = p2_start
        ball_reset()
        winner = ''
        difficulty = 0

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_SPACE]:
        new_game = False
        x_spd, y_spd = (settings['hor-ball-speed'], settings['ver-ball-speed'])
    if keys[pg.K_UP]:
        p2['y'] -= p_spd 
    if keys[pg.K_DOWN]: 
        p2['y'] += p_spd
    if keys[pg.K_w]:
        p1['y'] -= p_spd
    if keys[pg.K_s]:
        p1['y'] += p_spd
    if keys[pg.K_n]:
        new_game = True
    if keys[pg.K_m]:
        main_menu = True
        
    court_display(screen)

    if p1['score'] == score_limit or p2['score'] == score_limit:
        ball_reset()
        settings['net'] = False

    clock.tick(60)

    # check for border collision
    if ball['y'] < 0 or ball['y'] > s_height:
        court['color'] = (ri(0,255),ri(0,255),ri(0,255))
        y_spd += int(-y_spd*2)
    if ball['x'] < 0:
        ball_reset()
        ball['color'] = (ri(0,255),ri(0,255),ri(0,255))
        p1['x'], p1['y'] = p1_start
        p2['x'], p2['y'] = p2_start
        p1['score'] -= 1 if p1['score'] > 0 else 0
        p2['score'] += 1
    if ball['x'] > s_width:
        ball_reset()
        ball['color'] = (ri(0,255),ri(0,255),ri(0,255))
        p1['x'], p1['y'] = p1_start
        p2['x'], p2['y'] = p2_start
        p1['score'] += 1
        p2['score'] -= 1 if p2['score'] > 0 else 0

    # check for paddle collision
    if (ball['y'] + y_spd) in range(int(p1['y']), int(p1['y']+128)) and (ball['x']+x_spd) in range(int(p1['x']), int(p1['x']+40)):
        p1['color'] = (ri(0,255),ri(0,255),ri(0,255))
        x_spd += -int(x_spd*2)
    if (ball['y'] + y_spd) in range(int(p2['y']), int(p2['y']+128)) and (ball['x']+x_spd) in range(int(p2['x']-16), int(p2['x']+64)):
        p2['color'] = (ri(0,255),ri(0,255),ri(0,255))
        x_spd += -int(x_spd*2)
        
    if not new_game:
        ball['y'] += y_spd
        ball['x'] += x_spd

    if p1['score'] == score_limit:
        ball_reset()
        winner = f"{p1['name']} Won with {p1['score']}!"
    if p2['score'] == score_limit:
        ball_reset()
        winner = f"{p2['name']} Won with {p2['score']}!"
