countries = ["england","spain","france","germany","italy","netherlands","portugal"]
ind = 0
# data format:
# home team, away team, date, home team goals, away team goals
# sorted by dates

results_file = open("Individual Countries/"+countries[ind]+".csv",'r')
results = results_file.read().split('\n')[:-1]

start_rating = 1200
k,c = 32, 400
ratings = {}
peak_ratings = {}

for row in results:
    home_team,away_team,date,home_goals,away_goals = row.split(',')
    ratings[home_team] = [start_rating]
    ratings[away_team] = [start_rating]
    peak_ratings[home_team] = (1200,"")
    peak_ratings[away_team] = (1200,"")

for row in results:
    home_team,away_team,date,home_goals,away_goals = row.split(',')
    home_goals = int(home_goals)
    away_goals = int(away_goals)

    if home_goals==away_goals:
        home_score = 0.5
        away_score = 0.5
    elif home_goals>away_goals:
        home_score = 1
        away_score = 0
    elif home_goals<away_goals:
        home_score = 0
        away_score = 1

    home_rating = ratings[home_team][-1]
    away_rating = ratings[away_team][-1]

    home_expected = 1/(1+10**((away_rating-home_rating)/c))
    away_expected = 1/(1+10**((home_rating-away_rating)/c))
    
    home_new_rating = home_rating + k*(home_score-home_expected)
    away_new_rating = away_rating + k*(away_score-away_expected)

    ratings[home_team].append(home_new_rating)
    ratings[away_team].append(away_new_rating)

    if home_new_rating>peak_ratings[home_team][0]:
        peak_ratings[home_team] = (home_new_rating,date)
    
    if away_new_rating>peak_ratings[away_team][0]:
        peak_ratings[away_team] = (away_new_rating,date)

arr = [(team,peak_ratings[team][0],peak_ratings[team][1]) for team in peak_ratings]
arr.sort(key = lambda x:x[1])

l = len(arr)
for i in range(l):
    print(l-i,arr[i])