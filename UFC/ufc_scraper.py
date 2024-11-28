from bs4 import BeautifulSoup
from requests import get
from time import perf_counter as pc

# Storage format:
# non-draw: winner,loser
# draws not stored

save_file_path = "UFC_scrape_data.txt"
content = BeautifulSoup(get("http://www.ufcstats.com/statistics/events/completed?page=all").text,"html.parser")

event_tags = content.find_all(class_="b-link b-link_style_black")[:3]
total_events = len(event_tags)
event_count = 0


for tag in event_tags:
    s = pc()
    save_file = open(save_file_path,'a')

    event_link = tag['href']
    event_content = BeautifulSoup(get(tag['href']).text,"html.parser")

    win_tags = event_content.find_all(class_="b-flag b-flag_style_green")
    for wtag in win_tags:
        win_content = BeautifulSoup(get(wtag['href']).text,"html.parser")
        winner = win_content.find(class_="b-fight-details__person-status b-fight-details__person-status_style_green").parent.a.text[:-1]
        loser = win_content.find(class_="b-fight-details__person-status b-fight-details__person-status_style_gray").parent.a.text[:-1]
        save_file.write(f"{winner},{loser}\n")
    
    save_file.close()
    event_count+=1
    e = pc()
    print(f"{event_count}/{total_events} done in {round(e-s)} seconds")