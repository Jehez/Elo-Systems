from matplotlib.pyplot import plot,show,legend

from os import listdir
from json import load
folder_path = "tests_male_json"
files = listdir(folder_path)[:-1]

start_rating = 1200
k,c = 100, 4000
ratings = {}
peak_ratings = {}

# team_a, team_b, score_a, score_b, date
results = []

for file in files:
    f = open(folder_path+"/"+file,'r')
    match_info = load(f)["info"]
    f.close()

    outcome = match_info["outcome"]
    team_a, team_b = match_info["teams"]
    
    ratings[team_a] = [start_rating]
    ratings[team_b] = [start_rating]
    peak_ratings[team_a] = (start_rating,"")
    peak_ratings[team_b] = (start_rating,"")


    team_a, team_b = match_info["teams"]

    outcome = match_info["outcome"]
    if 'result' in outcome:
        score_a = 0.5
        score_b = 0.5
    else:
        winning_team = outcome['winner']
        if winning_team==team_a:
            score_a = 1
            score_b = 0
        else:
            score_a = 0
            score_b = 1
    
    date = match_info["dates"][-1]
    
    results.append([team_a,team_b,score_a,score_b,date])
results.sort(key=lambda x:x[-1])

for r in results:
    team_a, team_b, score_a, score_b, date = r

    team_a_rating = ratings[team_a][-1]
    team_b_rating = ratings[team_b][-1]

    team_a_expected = 1/(1+10**((team_b_rating-team_a_rating)/c))
    team_b_expected = 1/(1+10**((team_a_rating-team_b_rating)/c))

    team_a_new_rating = team_a_rating + k*(score_a-team_a_expected)
    team_b_new_rating = team_b_rating + k*(score_b-team_b_expected)

    ratings[team_a].append(team_a_new_rating)
    ratings[team_b].append(team_b_new_rating)

    if team_a_new_rating>peak_ratings[team_a][0]:
        peak_ratings[team_a] = (team_a_new_rating,date)
    
    if team_b_new_rating>peak_ratings[team_b][0]:
        peak_ratings[team_b] = (team_b_new_rating,date)

arr = [(team,peak_ratings[team][0],peak_ratings[team][1]) for team in peak_ratings]
arr.sort(key = lambda x:x[1])

l = len(arr)
for i in range(l):
    print(l-i,arr[i])

for t in ["India","Australia"]:
    plot(ratings[t],label=t)
legend()
show()