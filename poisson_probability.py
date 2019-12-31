'''
The goal here is to predict which teams will win by focusing on which teams will score the most goals or points, and allow the least of them.

There are a variety of different factors that correlate with high goal scoring, like possession of the ball, shots on goal and other relevant ones. In this example however, we will go with a much simpler approach as we will simply look at the previous scoring rates of teams (and goals allowed rates) and compare them to the league averages.
'''

import csv, math, ast, numpy as np

def poisson(actual, mean):
    return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)
    '''create function here that calculates of the probability of ‘actual’ amounts of goals scored, when the mean is equal to ‘mean’. This        writes out the probability ‘p’.
    '''
    
csvFile = <'FILENAME.csv'>

team_list = []

k = open('team_list.txt', 'w')
k.write("""{
""")
'''
a. Then we create an empty list, called team_list. 
b. Next we open a file named ‘team_list.txt’. You do not need to create this as if it does not exist, Python will create it. If it does exist, using the ‘w’ tag after the name ensures that it deletes all the info in the file and starts fresh.
c. Then we write the first line in the file, which is the start of a dictionary. This is needed to hold and update our data for each teams variables.
'''

csvRead = csv.reader(open(csvFile))
next(csvRead)

for row in csvRead:
	if row[2] not in team_list:
		team_list.append(row[2])
	if row[3] not in team_list:
		team_list.append(row[3])

team_list.sort()

for team in team_list:
	k.write("""	'%s': {'home_goals': 0, 'away_goals': 0, 'home_conceded': 0, 'away_conceded': 0, 'home_games': 0, 'away_games': 0, 'alpha_h': 0, 'beta_h': 0, 'alpha_a': 0, 'beta_a': 0},
""" % (team))

k.write("}")
k.close()

s = open('team_list.txt', 'r').read()
dict = ast.literal_eval(s)

'''
(a) Next we want to iterate over our data file and find all the team names that are going to be used (skip the first line and then create a for loop).

(b) The for loop simply reads both team names and then checks if the names are in our newly created team_list. If they are not, they get added to the list (append()).

(c) After it has checked all the team names, it sorts the new list alphabetically (sort()).

(d) Then it goes over to another for loop where it iterates over all the teams that have been found. For each team it will be written a line in the text file with different variables that we are going to use. In this example we will record all the home goals and away goals they score, as well as how many goals they concede both at home and away. We also track the amount of home and away games.

(e) Last we have some variables that calculate the scoring rate and concede rate for every team, and from this calculate probabilities of winning a game.

(f) We then write the end of the file and close it. This is so as to save what we have written if we want to open it again.

(g) The next two lines creates our dictionary where we will hold and update our data we read. This is done by using the ast module which will read the team_list.txt file and then create a dictionary called ‘dict’.
'''

GAMES_PLAYED = 0
WEEKS_WAIT = 4    # the number of weeks we wait before placing bets on the model
TOTAL_VALUE = 0   # will update and let us know how we're doing 


'''
Then we write a few variables we will use throughout the script. GAMES_PLAYED is simply the total tally of games played, WEEKS_WAIT is the number of weeks we want to wait before we start placing bets on our model and then TOTAL_VALUE will be used to update how are betting are doing.

Next we open another iteration of the data and skip the first line as usual, before we start with our main loop.
'''

csvRead = csv.reader(open(csvFile))
next(csvRead)

for game in csvRead:
	home_team = game[2]
	away_team = game[3]

	home_goals = int(game[4])
	away_goals = int(game[5])

	home_win_prob = 0
	draw_win_prob = 0
	away_win_prob = 0
	
	curr_home_goals = 0
	curr_away_goals = 0
	avg_home_goals = 1
	avg_away_goals = 1
	
	team_bet = ''
	ev_bet = ''
	
	# GETTING UPDATED VARIABLES
	for key, value in dict.items():
		curr_home_goals += dict[key]['home_goals']
		curr_away_goals += dict[key]['away_goals']
		
		if GAMES_PLAYED > (WEEKS_WAIT * 10):
			avg_home_goals = curr_home_goals / (GAMES_PLAYED)
			avg_away_goals = curr_away_goals / (GAMES_PLAYED)
	
	
	# CALCULATING FACTORS
	if GAMES_PLAYED > (WEEKS_WAIT * 10):
		home_team_a = (dict[home_team]['alpha_h'] + dict[home_team]['alpha_a']) / 2
		away_team_a = (dict[away_team]['alpha_h'] + dict[away_team]['alpha_a']) / 2
		
		home_team_d = (dict[home_team]['beta_h'] + dict[home_team]['beta_a']) / 2
		away_team_d = (dict[away_team]['beta_h'] + dict[away_team]['beta_a']) / 2
		
		home_team_exp = avg_home_goals * home_team_a * away_team_d
		away_team_exp = avg_away_goals * away_team_a * home_team_d
	
	
	# RUNNING POISSON	
		l = open('poisson.txt', 'w')
		
		for i in range(10):
			for j in range(10):
				prob = tau * poisson(i, home_team_exp) * poisson(j, away_team_exp)
				l.write("Prob%s%s = %s\n" % (i, j, prob))
		
		l.close()
		
		with open('poisson.txt') as f:
			for line in f:
				
				home_goals_m = int(line.split(' = ')[0][4])
				away_goals_m = int(line.split(' = ')[0][5])
				
				prob = float(line.split(' = ')[1])
				
				if home_goals_m > away_goals_m:
					home_win_prob += prob
				elif home_goals_m == away_goals_m:
					draw_win_prob += prob
				elif home_goals_m < away_goals_m:
					away_win_prob += prob

	#CALCULATE VALUE
		bet365odds_h, bet365odds_d, bet365odds_a = float(game[23]), float(game[24]), float(game[25])
		
		ev_h = (home_win_prob * (bet365odds_h - 1)) - (1 - home_win_prob)
		ev_d = (draw_win_prob * (bet365odds_d - 1)) - (1 - draw_win_prob)
		ev_a = (away_win_prob * (bet365odds_a - 1)) - (1 - away_win_prob)
		
		highestEV = max(ev_h, ev_d, ev_a)
		
		if (ev_h == highestEV) and (ev_h > 0):
			team_bet = home_team
			ev_bet = ev_h
			if home_goals > away_goals:
				TOTAL_VALUE += (bet365odds_h - 1)
			else:
				TOTAL_VALUE -= 1
				
		elif (ev_d == highestEV) and (ev_d > 0):
			team_bet = 'Draw'
			ev_bet = ev_d
			if home_goals == away_goals:
				TOTAL_VALUE += (bet365odds_d - 1)
			else:
				TOTAL_VALUE -= 1
		elif (ev_a == highestEV) and (ev_a > 0):
			team_bet = away_team
			ev_bet = ev_a
			if home_goals < away_goals:
				TOTAL_VALUE += (bet365odds_a - 1)
			else:
				TOTAL_VALUE -= 1
		
		if (team_bet != '') and (ev_bet != ''):
			print ("Bet on '%s' (EV = %s)" % (team_bet, ev_bet))	
			print (TOTAL_VALUE)
		
	# UPDATE VARIABLES AFTER MATCH HAS BEEN PLAYED
	dict[home_team]['home_goals'] += home_goals
	dict[home_team]['home_conceded'] += away_goals
	dict[home_team]['home_games'] += 1
	
	dict[away_team]['away_goals'] += away_goals
	dict[away_team]['away_conceded'] += home_goals
	dict[away_team]['away_games'] += 1
	
	GAMES_PLAYED += 1
	
	# CREATE FACTORS
	if GAMES_PLAYED > (WEEKS_WAIT * 10):
		for key, value in dict.items():
			alpha_h = (dict[key]['home_goals'] / dict[key]['home_games']) / avg_home_goals
			beta_h = (dict[key]['home_conceded'] / dict[key]['home_games']) / avg_away_goals

			alpha_a = (dict[key]['away_goals'] / dict[key]['away_games']) / avg_away_goals
			beta_a = (dict[key]['away_conceded'] / dict[key]['away_games']) / avg_home_goals

			dict[key]['alpha_h'] = alpha_h
			dict[key]['beta_h'] = beta_h
			dict[key]['alpha_a'] = alpha_a
			dict[key]['beta_a'] = beta_a
			
			#NameError: name 'tau' is not defined ?
