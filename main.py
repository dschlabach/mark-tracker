import requests
import os
import re
from bs4 import BeautifulSoup
import urllib.parse
import time

# used to track score
global mark_last_score
mark_last_score = ""

def send_message(message): 
  tg_url = "https://api.telegram.org/bot" + os.getenv("BOT_TOKEN") + "/sendMessage?chat_id=" + os.getenv("CHANNEL_ID") + "&text=" + urllib.parse.quote(message)
  requests.post(tg_url)

def check_score(): 
  url = "http://results.golfstat.com/public/leaderboards/gsnav.cfm?pg=teamPlayer&tid=20924"
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  mark_row = soup.find(string=re.compile("Mark Schlabach"))
  mark_score = mark_row.findNext('td').findNext('td').findNext('td').string
  global mark_last_score
  if mark_score == mark_last_score:
    print(mark_score)
    return
  else: 
    mark_over_under = re.findall('[^()]+', mark_score)[0]
    tg_message = "Mark is " + mark_over_under + "through " + mark_score[mark_score.find("(")+1:mark_score.find(")")] + " holes. \n \nSee the full scores here: " + url
    mark_last_score = mark_score
    print("sending message to group: ", tg_message)
    send_message(tg_message)

while True: 
  check_score()
  time.sleep(60)

