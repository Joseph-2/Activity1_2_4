#   leaderboard.py
# The leaderboard module to be used in a122 solution.

# set the levels of scoring

# load leaderboard from file
def score_evaluation(file_name,player_score,turtle_object,screen):
  player_score = str(player_score)
  font_setup = ("Arial", 15, "normal")
  highscore_file = open(file_name, "r")  # need to create the file ahead of time in same folder
  # use a for loop to iterate through the content of the file, one line at a time
  for line in highscore_file:
    high_score = line
  if int(player_score) > int(high_score):
    screen.bgpic("victory.gif")
    turtle_object.clear()
    turtle_object.write("Congratulations! You beat the high score!", font=font_setup)
    turtle_object.penup()
    turtle_object.sety(0)
    turtle_object.pendown()
    turtle_object.write("New high score is: "+player_score, font=font_setup)
    highscore_file = open(file_name, "w")
    highscore_file.write(player_score)
  else:
    screen.bgpic("unhappy-child.gif")
    turtle_object.clear()
    turtle_object.write("Sorry, you didn't beat the high score. Maybe next time!", font=font_setup)
    turtle_object.penup()
    turtle_object.sety(0)
    turtle_object.pendown()
    turtle_object.write("Your score was: "+player_score+". you need "+str(int(high_score)-int(player_score)+1)+" more to beat the high score of "+high_score, font=font_setup)
  highscore_file.close()