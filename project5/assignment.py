from pyspark import SparkContext
from functions import *
import re

sc = SparkContext("local", "Simple App")
setDefaultAnswer(sc.parallelize([0]))

## Load data into RDDs
playRDD = sc.textFile("datafiles/play.txt")
logsRDD = sc.textFile("datafiles/NASA_logs_sample.txt")
amazonInputRDD = sc.textFile("datafiles/amazon-ratings.txt")
nobelRDD = sc.textFile("datafiles/prize.json")

## The following converts the amazonInputRDD into 2-tuples with integers
amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()


### Task 1
print "=========================== Task 1"
task1_result = task1(playRDD)
for x in task1_result.takeOrdered(10):
	print x

### Task 2
print "=========================== Task 2"
task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap).distinct()
print task2_result.takeOrdered(10)

#### Task 3
print "=========================== Task 3"
task3_result = task3(nobelRDD)
for x in task3_result.takeOrdered(10):
	print x

#### Task 4
print "=========================== Task 4"
task4_result = task4(logsRDD, ['01/Jul/1995', '02/Jul/1995'])
for x in task4_result.takeOrdered(10):
	print x

#### Task 5
print "=========================== Task 5"
task5_result = task5(amazonBipartiteRDD)
print task5_result.collect()

#### Task 6
print "=========================== Task 6"
task6_result = task6(logsRDD, '01/Jul/1995', '02/Jul/1995')
for x in task6_result.takeOrdered(10):
	print x

#### Task 7
print "=========================== Task 7"
task7_result = task7(nobelRDD)
for x in task7_result.takeOrdered(10):
	print x

#### Task 8 -- we will start with a non-empty currentMatching and do a few iterations
print "=========================== Task 8"
currentMatching = sc.parallelize([('user1', 'product8')])
res1 = task8(amazonBipartiteRDD, currentMatching)
print "Found {} edges to add to the matching".format(res1.count())
print res1.takeOrdered(100)
currentMatching = currentMatching.union(res1)
res2 = task8(amazonBipartiteRDD, currentMatching)
print "Found {} edges to add to the matching".format(res2.count())
print res2.takeOrdered(100)
currentMatching = currentMatching.union(res2)
