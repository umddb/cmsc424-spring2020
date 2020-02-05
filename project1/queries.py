queries = ["" for i in range(0, 15)]

### 0. Report the three medalists and their winning times for ``100m Men's running'' at 2000 Olympics. Order by medalist names.
### Output column order: player_name, medal
queries[0] = """
select players.name as player_name, medal
from results, players, events
where events.name = '100m Men' and events.olympic_id = 'SYD2000' and results.player_id = players.player_id and events.event_id = results.event_id
order by player_name;
"""

### 1. Report the total number of medals won by M. Phelps over both olympics. 
### (Single) Output Column: num_medals.
queries[1] = """
select 0;
"""


### 2. For 2004 Olympics, generate a list - (birthyear, num_players, num_gold_medals) - containing the years in which the atheletes were born, 
### the number of players born in each year, and the number of gold medals won by the players born in each year.
### HINT: Use "extract" to operate on dates. Note you can use "extract" in a 'group by' clause as well.
### Order output by birthyear.
### Output columns: birthyear, num_players, num_gold_medals
queries[2] = """
select 0;
"""

### 3. For 2000 Olympics, find the 5 countries with the smallest values of ``number-of-medals/population''.
### Output columns: country_name, ratio
### Order by country name
queries[3] = """
select 0;
"""

### 4. Report all `individual events' where there was a tie in the score, and two or more players got awarded a Gold medal. 
### The 'Events' table contains information about whether an event is individual or not (Hint: Use ``group by'' and ``having'').
### Output Column: event_id, (event) name, olympic_id
### Order by: event_id
queries[4] = """
select 0;
"""

### 5,6. Team events are going to complicate our life, so we will create two new tables:
###             IndividualMedals(player_id, event_id, medal, result)
###             TeamMedals(country_id, event_id, medal, result)
### Write the queries (queries[5] and queries[6]) to create these two tables using the Results table. 
### Use the ``create table ... as'' command. 
### The TeamMedals table should only contain one entry for each country for each team event. Fortunately for us, 
### two teams from the same country can't compete in a team event. The information about whether an
### event is a team event is stored in the ``events'' table.
queries[5] = """
select 0;
"""

queries[6] = """
select 0;
"""

### 7. Write a query to find the players whose birthday was during the olympics they participated in. 
### Hint: Use `extract' function to operate on the dates.
### Output columns: player_name, birthdate, olympic_id
### Order by: player_name
queries[7] = """
select 0;
"""

### 8,9. Write a query (queries[8]) to add a new column called `country_id' to the IndividualMedals table. Initially the `country_id' column in the IndividualMedals table 
### would be listed as empty.  Write another query (queries[9]) to `update' the table to set it appropriately.
queries[8] = """
select 0;
"""

queries[9] = """
select 0;
"""

### 10. Which country had the largest percentage of players (who won a medal of course) whose names started with a vowel ?
### In other words, for each country, compute a ratio: "No. of players with names starting with a vowel"/"No. of players", and find the country with the largest ratio.
### The "who won a medal of course" is re-emphasizing that the dataset only contains players who won a medal.
### Output Column: Country Name
queries[10] = """
select 0;
"""

### 11. Find all athletes who won at least one of each medal (GOLD, SILVER and BRONZE) at a single Olympics. 
### Output Columns: player_name, olympic_id
### Order by: player_name
queries[11] = """
select 0;
"""

### 12. In the individual events where the result was noted in seconds, write a query to find which Gold Medal winning player had the largest margin of 
### victory over the Silver medal. Be careful -- there are events where there was no Silver medal, but multiple Gold medals were awarded. You might want to 
### create a temporary table using WITH ``temp(event_id, gold_player_id, gold_result, silver_result)''.
### Output columns: player_name
queries[12] = """
select 0;
"""

### 13. Write a query to find for all countries, the total number of medals it won and the `rank' of the country 
### by that metric (i.e., the country with the largest number of medals is ranked 1, etc). If two countries tie, 
### they get the same rank, and the next rank is skipped.
### Output columns: country_name, num_medals, rank
### Output order: ascending by rank
### HINT: There is a special operator in SQL to help with this.
queries[13] = """
select 0;
"""
