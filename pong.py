# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0
ball_color = "White"
party_mode = False

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(2,5), random.randrange(-3,0)]
    if direction == "LEFT":
        ball_vel[0] = -1*ball_vel[0]
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = [0, HEIGHT/2]
    paddle2_pos = [WIDTH, HEIGHT/2]
    spawn_ball(random.choice(["LEFT","RIGHT"]))

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global party_mode, ball_color
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
                 
    # draw ball
    if party_mode:
        ball_color = random.choice (["White", "Red", "Blue", "Yellow"])
    else:
        ball_color = "White"
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", ball_color)
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    if paddle2_pos[1] <= PAD_HEIGHT/2:
        paddle2_pos[1] = PAD_HEIGHT/2
    if paddle2_pos[1] >= HEIGHT - PAD_HEIGHT/2:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT/2
    if paddle1_pos[1] <= PAD_HEIGHT/2:
        paddle1_pos[1] = PAD_HEIGHT/2
    if paddle1_pos[1] >= HEIGHT - PAD_HEIGHT/2:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT/2
    
    
    # draw paddles
    pad1_points = [[0, paddle1_pos[1]-PAD_HEIGHT/2], [0, paddle1_pos[1]+PAD_HEIGHT/2]]
    pad2_points = [[WIDTH, paddle2_pos[1]-PAD_HEIGHT/2], [WIDTH, paddle2_pos[1]+PAD_HEIGHT/2]]
    c.draw_line(pad1_points[0], pad1_points[1], PAD_WIDTH*2, "White")
    c.draw_line(pad2_points[0], pad2_points[1], PAD_WIDTH*2, "White")
    # draw scores
    c.draw_text(str(score1), (100,100), 60, "Magenta")
    c.draw_text(str(score2), (WIDTH-100,100), 60, "Magenta")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -1*ball_vel[1]
    if ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = -1*ball_vel[1]        
    
    
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
       # if abs(ball_pos[1]-paddle1_pos[1]) <= (PAD_WIDTH+BALL_RADIUS):
        if abs(ball_pos[1]-paddle1_pos[1]) <= (PAD_HEIGHT/2):
            
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 +=1
            spawn_ball("RIGHT")
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
       # if abs(ball_pos[1]-paddle2_pos[1]) <= (PAD_WIDTH + BALL_RADIUS):    
        if abs(ball_pos[1]-paddle2_pos[1]) <= (PAD_HEIGHT/2):         
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:        
            score1 +=1
            spawn_ball("LEFT")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
   
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    
def reset():
    new_game()
    
def party():
    global party_mode, ball_color
    party_mode = not party_mode
           

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 100)
frame.add_button("Party Ball", party, 100)
frame.add_label('Player one: Keys "w" and "s". Player two: arrow keys')


# start frame
new_game()
frame.start()
