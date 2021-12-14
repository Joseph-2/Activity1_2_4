# Imports/Classes
import turtle as trtl
import random as rand
import highscore as hs


class Er(Exception):
    pass

# Variables - - - - - - - - - - - - - - - - - - -


while True:
    try:
        difficulty = int(
            input("Choose between difficulty 1(easy), 2(normal), or 3(hard): "))

        if difficulty == 1:
            fruit_dis = 5
            fruit_speed = "slow"

        elif difficulty == 2:
            fruit_dis = 20
            fruit_speed = "normal"

        elif difficulty == 3:
            fruit_dis = 30
            fruit_speed = 0

        else:
            raise Er(Exception)
        break

    except Er:
        print("please only choose between said aforementioned difficulties")

    except ValueError:
        print("please only choose between said aforementioned difficulties")

fruitz = ["apple.gif", "cherry.gif", "orange.gif", "pear.gif", "banana.gif"]

score = 0

font_setup = ("Arial", 15, "normal")

timer = 5

counter_interval = 1000  # 1000 represents 1 second

score_file = "LB.txt"

# did the timer run out?
timer_up = False

# did someone click the start button?
game_start_clicked = False

# is this our first fruit?
game_begin = False

# was the fruit clicked since our last update?
fruit_clicked = False

# Turtle Configuration - - - - - - - - - -

wn = trtl.Screen()
wn.setup(width=1500, height=800)
wn.bgpic("fruit_ninja.gif")
wn.addshape("game_start.gif")
for x in fruitz:
    wn.addshape(x)

active_fruit = trtl.Turtle()
active_fruit.hideturtle()
active_fruit.speed(fruit_speed)
active_fruit.penup()

start_game = trtl.Turtle()
start_game.pu()
start_game.speed(8)
start_game.hideturtle()
start_game.shape("game_start.gif")

score_writer = trtl.Turtle()
score_writer.hideturtle()
score_writer.pu()
score_writer.goto(-700, 350)
score_writer.pd()
score_writer.color("white")

counter = trtl.Turtle()
counter.hideturtle()
counter.color("white")
counter.penup()
counter.goto(600, 350)
counter.pendown()

# Functions - - - - - - - - - - - - - -


def manage_highscore():
    global score
    hs.score_evaluation(score_file, score, score_writer, wn)


def new_fruit():
    #print("Getting a new fruit")
    # assume turtle is hidden -- moves fruit to the top, allocates a new shape
    #print("Getting random x position")
    randomx = rand.randint(-500, 500)
    # active_fruit.speed(fruit_speed)
    #print(f"Moving new fruit to {randomx},400")
    active_fruit.goto(randomx, 400)
    #print("getting a random fruit type")
    random_fruit = rand.randint(0, 4)
    #print(f"Setting fruit to fruit {random_fruit}")
    active_fruit.shape(fruitz[random_fruit])
    #print("Done getting new fruit")


def fruitloop():
    global timer_up, fruit_clicked, game_begin

    if game_begin:
        #print("in game begin")
        game_begin = False
        # get a new fruit
        new_fruit()
        # write out initial score
        update_score()
        # attach the click handler
        active_fruit.onclick(fruit_click_handler)
        # show the turtle
        active_fruit.showturtle()
        # start the countdown
        countdown()
    elif timer_up is True:
        # all done, hide any fruit
        active_fruit.hideturtle()
        # handle high score/leaderboards
        score_writer.color("black")
        manage_highscore()
        # don't schedule another tick
        return
    elif fruit_clicked:
        #print("Fruit was clicked")
        # fruit was clicked, hide the fruit, bump the score, reset clicked, get new fruit
        active_fruit.hideturtle()
        update_score(True)
        # reset so the player can score again
        fruit_clicked = False
        new_fruit()
        active_fruit.showturtle()
    else:
        # otherwise, move current fruit
        # get current y-position
        ycor = int(active_fruit.ycor())

        # if we are still on-screen...
        if ycor > -400:
            # fruit is visible, update position
            ycor = ycor - fruit_dis
            active_fruit.sety(ycor)
        else:
            # fruit fell off the screen
            # hide the fruit
            active_fruit.hideturtle()
            # take a point away
            update_score(False)
            # get a new fruit
            new_fruit()
            # show it
            active_fruit.showturtle()
    # schedule the loop to run again in 16ms -- 16ms per update == about 60 updates per second
    wn.ontimer(fruitloop, 16)


def update_score(scored_point=None):
    global score
    if scored_point is not None:
        if scored_point is True:
            #print("Scored a point")
            score += 1
        else:
            #print("Lost a point")
            score -= 1
    score_writer.clear()
    score_writer.write(score, font=font_setup)


def fruit_click_handler(x, y):
    #print("fruit click handler")
    global fruit_clicked
    if fruit_clicked:
        #print("Fruit extra click")
        # ignore a second click
        return
    #print("Fruit clicked!")
    fruit_clicked = True


def countdown():
    global timer, timer_up
    #print("Timer tick")
    counter.clear()
    if timer <= 0:
        counter.write("Time's Up", font=font_setup)
        timer_up = True
    else:
        counter.write("Timer: " + str(timer), font=font_setup)
        timer -= 1
        counter.getscreen().ontimer(countdown, counter_interval)
    #print("end timer tick")


def start_click(x, y):
    global game_start_clicked, game_begin
    # get rid of the clear screen amimation
    start_game.hideturtle()
    start_game.goto(0, -1000)
    start_game.clear()
    # exit the game start animation
    game_start_clicked = True
    # let draw_fruit know we're starting off
    game_begin = True

    fruitloop()


def gamestart_anim():
    start_game.showturtle()

    while game_start_clicked == False:
        start_game.circle(20)

# Events -------------------


start_game.onclick(start_click)

gamestart_anim()

wn.mainloop()
