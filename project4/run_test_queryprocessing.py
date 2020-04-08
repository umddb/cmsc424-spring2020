import os
import sys
import traceback
from functools import wraps
import errno
import signal

from disk_relations import *
from queryprocessing import *
from btree import *

# A simple class to keep track of the set of relations and indexes created together
class Database:
    def __init__(self, name):
        self.name = name
        self.relations = dict()
        self.indexes = dict()
    def newRelation(self, relname, rel_schema):
        self.relations[relname] = Relation(relname, rel_schema)
        return self.relations[relname]
    def getRelation(self, relname):
        return self.relations[relname]
    def newIndex(self, relname, attribute, keysize):
        self.indexes[(relname, attribute)] = BTreeIndex(keysize = keysize, relation = self.getRelation(relname), attribute = attribute)
        return self.indexes[(relname, attribute)]
    def getIndex(self, relname, attribute):
        return self.indexes[(relname, attribute)]

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


######################### COMARING ANSWERS
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
         if t1[i] is None or t2[i] is None: 
            if t1[i] is not None or t2[i] is not None:
                return False
         elif int(t1[i]) != int(t2[i]):
            return False
     return True


def compare(ans, expected_output):
    print("Comparing {} and {}".format(ans, expected_output))
    if len(ans) != len(expected_output):
        return False
    if len(ans) == 0:
        return True
    for eo in expected_output:
        found = None
        for a in ans:
            if compare_two_tuples(a.t, eo):
                 found = a
                 break
        if found is None:
            return False
        else:
            ans.remove(a)
    return True

def create_single_attribute_relation(name, attr, tuples):
    r = db.newRelation(name, [attr])
    for t in tuples:
        r.insertTuple(Tuple([attr], t))
    return r

def create_two_attribute_relation(name, attrs, tuples):
    r = db.newRelation(name, attrs)
    for t in tuples:
        r.insertTuple(Tuple(attrs, (str(t[0]), str(t[1]))))
    return r

def run_one_test(q, expected_output):
    try:
        q.init()
        print("--------------------------------------------------------------------- Executing Query {}".format(str(q)))
        ans = collectAll(q)
        if compare(ans, expected_output):
             print("Success")
        else:
             print("Failed")
    except:
            exception = "Runtime error:\n {}\n {}\n {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
            print(traceback.format_exc())

######################### START TESTING
db = Database("Test")

aggregate_relation = create_single_attribute_relation("L1", "A", [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)])
avg_result = [(5)]

hj_r = create_two_attribute_relation("R1", ["A", "B"], [(-1, 1), (-1, 2)])
hj_s = create_two_attribute_relation("S1", ["B", "C"], [(2, -1), (3, -1)])
hj_results = [(-1, 1, None, None), (-1, 2, 2, -1), (None, None, 3, -1)]

si_x = create_two_attribute_relation("X1", ["A", "B"], [(1, 2), (1, 3)])
si_y = create_two_attribute_relation("Y1", ["A", "B"], [(1, 1), (1, 2)])
si_results = [(1, 2)]


run_one_test(GroupByAggregate(SequentialScan(aggregate_relation), "A", GroupByAggregate.AVERAGE), avg_result)
run_one_test(HashJoin(SequentialScan(hj_r), SequentialScan(hj_s), "B", "B", HashJoin.FULL_OUTER_JOIN), hj_results)
run_one_test(SetIntersection(SequentialScan(si_x), SequentialScan(si_y), False), si_results)

