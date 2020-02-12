import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse

from queries import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', help="Run queries one at a time, and wait for user to proceed", required=False, action="store_true")
parser.add_argument('-q', '--query', type = int, help="Only run the given query number", required=False)
args = parser.parse_args()

interactive = args.interactive

conn = psycopg2.connect("dbname=olympics user=vagrant")
cur = conn.cursor()

totalscore = 0
for i in range(0, 14):
    # If a query is specified by -q option, only do that one
    if args.query is None or args.query == i:
        try:
            if interactive:
                os.system('clear')
            print("========== Executing Query {}".format(i))
            print(queries[i])
            cur.execute(queries[i])

            if i not in [5, 6, 8, 9]:
                ans = cur.fetchall()

                print("--------- Your Query Answer ---------")
                for t in ans:
                    print(t)
                print("")
            else:
                if i in [5, 8, 9]:
                    conn.commit()
                    print("--------- Running SELECT * FROM IndividualMedals LIMIT 5 -------")
                    cur.execute("select * from IndividualMedals limit 5")
                    ans = cur.fetchall()
                    print("-- Result")
                    for t in ans:
                        print(t)
                    print("")
                if i == 6:
                    conn.commit()
                    print("--------- Running SELECT * FROM TeamMedals LIMIT 5 -------")
                    cur.execute("select * from TeamMedals limit 5")
                    ans = cur.fetchall()
                    print("-- Result")
                    for t in ans:
                        print(t)
                    print("")
                
            if interactive:
                input('Press enter to proceed')
                os.system('clear')
        except:
            print(sys.exc_info())
            raise
