## Project 1: SQL Assignment, CMSC424, Fall 2016

*The assignment is to be done by yourself.*

The following assumes you have gone through PostgreSQL instructions and have ran some queries on the `university` database. 
It also assumed you have cloned the git repository, and have done a `git pull` to download the directory `project1`. The files are:

1. README.md: This file
1. populate.sql: The SQL script for creating the data.
1. queries.py: The file where to enter your answer
1. SQLTesting.py: File to be used for running the queries (in `queries.py`) against the database, and generate the file to be submitted.
1. Vagrantfile: A Vagrantfile that creates the `olympics` database and populates it using `populate.sql` file.

### Getting started
Start the VM with `vagrant up` in the `project1/` directory. The database should already be set up, but if not: 
- Create a new database called `olympics` and switch to it (see the PostgreSQL setup instructions).
- Run `\i populate.sql` to create and populate the tables. 

### Schema 
The dataset contains the details of the 2000 and 2004 Summer Olympics, for a subset of the games (`swimming` and `athletics`). More specifically,
it contains the information about `players`, `countries`, `events`, and `results`. It only contains the medals information
(so no heats, no players who didn't win a medal).

The schema of the tables should be self-explanatory. 

The data was collected from http://www.databaseolympics.com/ and Wikipedia.

Some things to remember: 
- The birth-date information was not available in the database, and that field was populated randomly.
- Be careful with the team events; the information about medals is stored by player, and a single team event gold gets translated into usually 4, but upto 6-7 `medal` entries in the Results table (for SWI and ATH events).
- If two players tie in an event, they are both awarded the same medal, and the next medal is skipped (i.e., there are events without any silver medals, but two gold medals). This is more common in Gymnastics (we don't have that data).
- The `result` for a match is reported as a `float` number, and its interpretation is given in the corresponding
`events` table. There are three types: `seconds` (for time), `points` (like in Decathlon), `meters` (like in long jump).


In many cases (especially for complex queries or queries involving 
`max` or `min`), you will find it easier to create temporary tables
using the `with` construct. This also allows you to break down the full
query and makes it easier to debug.

You don't have to use the "hints" if you don't want to; there might 
be simpler ways to solve the questions.

### Testing and submitting using SQLTesting.py
Your answers (i.e., SQL queries) should be added to the `queries.py` file. A simple query is provided for the first answer to show you how it works.
You are also provided with a Python file `SQLTesting.py` for testing your answers.

- We recommend that you use `psql` to design your queries, and then paste the queries to the `queries.py` file, and confirm it works.

- SQLTesting takes quite a few options: use `python3 SQLTesting.py -h` to see the options.

- To get started with SQLTesting, do: `python3 SQLTesting.py -v -i` -- that will run each of the queries and show you your answer.

- If you want to run your query for Question 1, use: `python3 SQLTesting.py -q 1`. 

- `-i` flag to SQLTesting will run all the queries, one at a time (waiting for you to press Enter after each query).

- **Note**: We will essentially run a modified version of `SQLTesting.py` that compares the returned answers against correct answers. So it imperative that `python3 SQLTesting.py` runs without errors.

### Submission Instructions
Submit the `queries.py` file using ELMS.
      
### Assignment Questions
See `queries.py` file.
