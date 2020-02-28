import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse
import pickle

import importlib

from queries import *

with open("correct_answers.pickle", "rb") as f:
    correct_answers = pickle.load(f)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', help="Run queries one at a time, and wait for user to proceed", required=False, action="store_true")
parser.add_argument('-q', '--query', type = int, help="Only run the given query number", required=False)
args = parser.parse_args()

interactive = args.interactive

conn = psycopg2.connect("dbname=olympics user=vagrant")
cur = conn.cursor()

query_im = """
create table if not exists IndividualMedals as
    select player_id, e.event_id, medal, result
    from results r, events e
    where r.event_id = e.event_id and is_team_event = 0
"""

query_tm = """
create table if not exists TeamMedals as 
    select distinct country_id, e.event_id, medal, result
    from results r, events e, players p
    where r.event_id = e.event_id and r.player_id = p.player_id and is_team_event = 1
"""

cur.execute(query_im)
cur.execute(query_tm)
conn.commit()

answers = [None] * 14

totalscore = 0
for i in range(1, 14):
    # If a query is specified by -q option, only do that one
    if i not in [5, 6, 8, 9]:
        if args.query is None or args.query == i:
            try:
                if interactive:
                    os.system('clear')
                print("========== Executing Query {}".format(i))
                print(queries[i])
                cur.execute(queries[i])

                ans = cur.fetchall()
                answers[i] = ans

                print("--------- Your Query Answer ---------")
                for t in ans:
                    print(t)
                print("")

                print("--------- Correct Query Answer ---------")
                for t in correct_answers[i]:
                    print(t)
                print("")
            except:
                print(sys.exc_info())


cur.execute("drop table IndividualMedals;")
cur.execute("drop table TeamMedals;")
conn.commit()

for i in range(1, 14):
    # If a query is specified by -q option, only do that one
    if i in [5, 6, 8, 9]:
        if args.query is None or args.query == i:
            try:
                print("========== Executing Query {}".format(i))
                print(queries[i])
                cur.execute(queries[i])

                conn.commit()

                if i in [5, 8, 9]:
                    print("--------- Running SELECT * FROM IndividualMedals LIMIT 5 -------")
                    cur.execute("select * from IndividualMedals limit 5")
                    ans = cur.fetchall()
                    answers[i] = ans
                    print("--------- Your Query Answer")
                    for t in ans:
                        print(t)
                    print("")
                    print("--------- Correct Query Answer ---------")
                    for t in correct_answers[i]:
                        print(t)
                    print("")
                if i == 6:
                    print("--------- Running SELECT * FROM TeamMedals LIMIT 5 -------")
                    cur.execute("select * from TeamMedals limit 5")
                    ans = cur.fetchall()
                    answers[i] = ans
                    print("--------- Your Query Answer")
                    for t in ans:
                        print(t)
                    print("")
                    print("--------- Correct Query Answer ---------")
                    for t in correct_answers[i]:
                        print(t)
                    print("")
                    
                if interactive:
                    input('Press enter to proceed')
                    os.system('clear')
            except:
                print(sys.exc_info())

#with open("correct_answers", "wb") as f:
#    pickle.dump(answers, f)

