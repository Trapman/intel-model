# first thing we need to do is import data, usually from a CSV

import csv

csv_file = csv.reader(open( '<FILE NAME>' ))
next(csv_file)

upsets = 0
non_upsets = 0

starting_bankroll = 100
wagering_size = 5

bankroll = starting_bankroll

'''
Now we get to core of things when we introduce a for loop to our current code. Basically what this does is that it iterates over every instance that you set for it. You could say that you want to run a code 10 times, and then use a for loop with a range(0, 9).

What we want though is to read over every game (or line of data) and do something to every game. Also, for every iteration of games we want to store parts of the data in different variables. Team names, number of goals scored, betting odds and other things. This is done by using the variable name we set when looping over the csv_file, which is game, and grab the column we want for that specific line.

In short, each column in a csv file can be thought of as an index. So if we want the very first column was use csv[0], if we want the last then we use csv[-1], if we want the third we use csv[2] and so forth. 
'''

#all of these game[] just refer to the column in the CSV that we want to pull from. We'll need to do some int() and float() conversions
for game in csv_file:
	home_team = game[2]
	away_team = game[3]

	home_goals = int(game[4])
	away_goals = int(game[5])

	home_odds = float(game[23])
	draw_odds = float(game[24])
	away_odds = float(game[25])
  
'''
In this model we are looking for home underdogs, which is when the odds of a home team win is higher than an away team win.

To do this, we use what is called an if function. Basically what it does is that it takes a condition that needs to be met, and if that is true, then it runs some code, otherwise it does something else, which can be nothing.
'''

if home_odds > away_odds:
  upsets += 1
  bankroll += wagering_size * (home_odds - 1)
  
else:
  non_upsets += 1
  bankroll -= wagering_size
  
'''
So we're doing is looking at a game and comparing the odds of the home team winning and the odds of the away team winning. If there is higher odds for a home win, we proceed, if not, we ignore that game.

Then we check to see if the game ended in a win. This is done by testing if there were more home goals than away goals. If it was, we add 1 to our counter for home underdog wins (which we have called upsets). We also update our bankroll as if we would have bet on that game. Here we multiply our bet size with the odds we would have gotten.

Here we also have an else function added for those times the home team does NOT win. Here we add to the counter for non home underdog wins (named non_upsets) and also update the bankroll as if we would have wagered on it and thus lost in this case.
'''

print ("Starting bankroll = '%s'" % (starting_bankroll))

ROI = ((bankroll - starting_bankroll) / (wagering_size * (upsets + non_upsets))) * 100		

print ("There were '%s' upsets out of '%s' total matches" % (upsets, upsets + non_upsets))
print ("Starting bankroll = '%s'" % (starting_bankroll))
print ("Finishing bankroll = '%s' | ROI = '%s'" % (bankroll, ROI))
