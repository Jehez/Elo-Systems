results_file = open("UFC_scrape_data.txt",'r')
results = results_file.read().split('\n')[:-1][::-1]

start_rating = 1200
k,c = 32, 400
ratings = {}
peak_ratings = {}

for r in results:
    f1,f2 = r.split(',')
    ratings[f1] = [start_rating]
    ratings[f2] = [start_rating]

for r in results:
    f_a,f_b = r.split(',')
    r_a,r_b = ratings[f_a][-1],ratings[f_b][-1]
    e_a = 1/(1+10**((r_b-r_a)/c))
    e_b = 1/(1+10**((r_a-r_b)/c))
    new_r_a = r_a + k*(1-e_a)
    new_r_b = r_b + k*(0-e_b)
    ratings[f_a].append(new_r_a)
    ratings[f_b].append(new_r_b)
    peak_ratings[f_a] = max(ratings[f_a])
    peak_ratings[f_b] = max(ratings[f_b])

arr = [(f,peak_ratings[f]) for f in ratings]
arr.sort(key=lambda x:x[-1],reverse=False)

for i in range(len(arr)):
    print(len(arr)-i,arr[i])