import json
import math
import os
import random
import re
import subprocess
import sys
import traceback
from functools import wraps
import errno
import signal
import pickle

import copy

from pyspark import SparkContext
from functions import *


results_json = {"tests": [ ]} 

def add_test_result(test_no, score, max_score, output):
    results_json['tests'].append({"score": score, "max_score": max_score, "name": "", "number": test_no, "output": output}) 

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
########################################

@timeout(10)
def collectAll(plan):
    ret = list()
    plan.init()
    for t in plan.get_next():
        ret.append(t)
    return ret

def compare_two_tuples(t1, t2):
     print("=== Comparing {} and {}".format(t1, t2))
     if t1 is None or t2 is None:
        return t1 is None and t2 is None
     if type(t1) not in [tuple, list] or type(t2) not in [tuple, list]:
         if type(t1) in [tuple, list] or type(t2) in [tuple, list]:
             return False
         else:
             return abs(float(t1) - float(t2)) < .5

     if len(t1) != len(t2):
        return False
     for i in range(0, len(t1)):
        #print("-- {} -- {}".format(t1[i], t2[i]))
         if t1[i] is None or t2[i] is None: 
            if t1[i] is not None or t2[i] is not None:
                return False
         elif int(t1[i]) != int(t2[i]):
            return False
     return True

def compare_two_as_strings(t1, t2):
    return str(t1) == str(t2)

def compare(ans, expected_output):
    print("Comparing {} and {}".format(ans, expected_output))
    if len(ans) != len(expected_output):
        return False
    if len(ans) == 0:
        return True
    for eo in expected_output:
        found = None
        for a in ans:
            if compare_two_as_strings(a, eo):
                 found = a
                 break
        if found is None:
            return False
        else:
            ans.remove(a)
    return True


all_found_answers = []

def run_one_test(func, expected_output, test_no, max_score):
    try:
	print("=========================== Task {}".format(test_no))
        ans = func()
        all_found_answers.append(copy.deepcopy(ans))
        for t in ans:
            print(t)

        if compare(ans, expected_output):
             print("Success")
             add_test_result("Task {}".format(test_no), max_score, max_score, "Success")
        else:
             print("Failed")
             add_test_result("Task {}".format(test_no), 0, max_score, "Failed -- Answer Didn't Match Expected Output")
    except:
            exception = "Runtime error:\n {}\n {}\n {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
            add_test_result("{}".format(test_no), 0, max_score, "Failed -- Exception {}".format(traceback.format_exc()))
            print(traceback.format_exc())

def execute_task1():
	playRDD = sc.textFile("datafiles/play.txt")
	task1_result = task1(playRDD)
        return task1_result.takeOrdered(10)

def execute_task2():
	nobelRDD = sc.textFile("datafiles/prize.json")
	task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap).distinct()
        return [x.encode('utf-8') for x in task2_result.takeOrdered(10)]

def execute_task3():
	nobelRDD = sc.textFile("datafiles/prize.json")
	task3_result = task3(nobelRDD)
        ret = task3_result.takeOrdered(10)
        ret_sorted = [(x[0], sorted(x[1])) for x in ret]
        return ret_sorted

def execute_task4():
	logsRDD = sc.textFile("datafiles/NASA_logs_sample.txt")
	task4_result = task4(logsRDD, ['01/Jul/1995', '02/Jul/1995'])
        return [x.encode('utf-8') for x in task4_result.takeOrdered(10)]

def execute_task5():
	amazonInputRDD = sc.textFile("datafiles/amazon-ratings.txt")
	amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()
	task5_result = task5(amazonBipartiteRDD)
        return task5_result.takeOrdered(10)

def execute_task6():
	logsRDD = sc.textFile("datafiles/NASA_logs_sample.txt")
	task6_result = task6(logsRDD, '01/Jul/1995', '02/Jul/1995')
        ret = task6_result.takeOrdered(10)
        ret_sorted = [(x[0], (sorted(x[1][0]), sorted(x[1][1]))) for x in ret]
        return ret_sorted

def execute_task7():
	nobelRDD = sc.textFile("datafiles/prize.json")
	task7_result = task7(nobelRDD)
        return task7_result.takeOrdered(10)

def execute_task8():
	#### Task 8 -- we will start with a non-empty currentMatching and do a few iterations
	amazonInputRDD = sc.textFile("datafiles/amazon-ratings.txt")
	amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()
	currentMatching = sc.parallelize([('user1', 'product8')])
	res1 = task8(amazonBipartiteRDD, currentMatching)
	print "Found {} edges to add to the matching".format(res1.count())
        first = res1.takeOrdered(100)

	currentMatching = currentMatching.union(res1)
	res2 = task8(amazonBipartiteRDD, currentMatching)
	print "Found {} edges to add to the matching".format(res2.count())
        second = res2.takeOrdered(100)

        return first + second

sc = SparkContext("local", "Simple App")
setDefaultAnswer(sc.parallelize(["0"]))

with open('small_results.pickle', 'rb') as token:
     all_answers = pickle.load(token)

for ix, f in enumerate([execute_task1, execute_task2, execute_task3, execute_task4, execute_task5, execute_task6, execute_task7, execute_task8]):
    score = 5
    if ix == 8: score = 0
    if ix == 7: score = 10

    if ix < len(all_answers):
        run_one_test(f, all_answers[ix], (ix+1), score)
    else: 
        run_one_test(f, [], (ix+1), score)


#with open('small_results.pickle', 'wb') as token:
#    pickle.dump(all_found_answers, token)

print(results_json)
