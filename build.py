import requests, json
import pandas as pd
from pprint import pprint

# base url for all FPL API endpoints
base_url = 'https://fantasy.premierleague.com/api/'
player_stats_extension = 'event/{GW}/live/'

# get data from bootstrap-static endpoint
r = requests.get(base_url+'bootstrap-static/').json()
print(type(r))

# show the top level fields
#pprint(r, indent=2, depth=1, compact=True)

players = r['elements']
teams = r['teams']
print(type(players))

for x in range(10):
    print(f'id:{players[x]['id']} | name:{players[x]['web_name']} | minutees played:{players[x]['minutes']} | goals:{players[x]['goals_scored']} | \
points:{players[x]['total_points']} | assists:{players[x]['assists']} | price:{players[x]['now_cost']/10} |\n\n')
    
print(teams[0])