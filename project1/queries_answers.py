queries = ["" for i in range(0, 15)]

### 0. Report the three medalists and their winning times for ``100m running'' at 2000 Olympics. Order by medalist names.
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
select count(medal) 
from results 
where player_id = 'PHELPMIC01';
"""


### 2. For 2004 Olympics, generate a list - (birthyear, num_players, num_gold_medals) - 
### containing the years in which the atheletes were born, 
### the number of players born in each year, and the number of gold medals won by 
### the players born in each year.
### HINT: Use "extract" to operate on dates.
### Order output by birthyear.
### Output columns: birthyear, num_players, num_gold_medals

queries[2] = """
select extract(year from birthdate) as birthyear, count(distinct players.player_id) as num_players, count(case when results.medal = 'GOLD' then 1 end)
from players, results, events
where players.player_id = results.player_id and events.event_id = results.event_id and events.olympic_id = 'ATH2004'
group by extract(year from birthdate)
"""

### 3. For 2000 Olympics, find the 5 countries with the smallest values of ``number-of-medals/population''.
### Output columns: country_name, ratio
### Order by country name
queries[3] = """
with temp1 as (
    (select p.country_id, im.medal
     from IndividualMedals im, players p, events e
     where  p.player_id = im.player_id and im.event_id = e.event_id and e.olympic_id = 'SYD2000'
     )
    union ALL
    (select tm.country_id, tm.medal
     from TeamMedals tm, events e
     where tm.event_id = e.event_id and e.olympic_id = 'SYD2000'
    )
),
temp2 as (
    select c.name, c.country_id, count(*)/cast(c.population as float) as ratio
    from temp1, countries c
    where temp1.country_id = c.country_id
    group by c.country_id, c.name, c.population
)
select name, ratio
from temp2 t1
where 5 > (select count(*) from temp2 t2 where t2.ratio < t1.ratio)
order by name
"""

### 4. Report all `individual events' where there was a tie in the score, 
### and two or more players got awarded a Gold medal. 
### The 'Events' table contains information about whether an event is 
### individual or not (Hint: Use ``group by'' and ``having'').
### Output Column: event_id, (event) name, olympic_id
### Order by: event_id
queries[4] = """
select name, olympic_id
from events 
where is_team_event = 0 and event_id in (
    select event_id
    from results
    where medal like '%GOLD%'
    group by event_id 
    having count(medal) > 1
)
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
create table if not exists IndividualMedals as
    select player_id, e.event_id, medal, result
    from results r, events e
    where r.event_id = e.event_id and is_team_event = 0
"""

queries[6] = """
create table if not exists TeamMedals as 
    select distinct country_id, e.event_id, medal, result
    from results r, events e, players p
    where r.event_id = e.event_id and r.player_id = p.player_id and is_team_event = 1
"""

### 7. Write a query to find the players whose birthday was during 
### the olympics they participated in. 
### Hint: Use `extract' function to operate on the dates.
### Output columns: player_name, birthdate, olympic_id
### Order by: player_name

queries[7] = """
with temp as (
    select p.name as player_name, birthdate, o.olympic_id as olympic_id, startdate, enddate 
    from players p, events e, results r, olympics o 
    where p.player_id = r.player_id and r.event_id = e.event_id and e.olympic_id = o.olympic_id
) 
select distinct player_name, birthdate, olympic_id 
from temp
where extract(year from age(startdate - 1, birthdate)) != extract(year from age(enddate, birthdate))
order by player_name; 
"""

### 8,9. Write a query (queries[8]) to add a new column called `country_id' to the IndividualMedals table. Initially the `country_id' column in the IndividualMedals table 
### would be listed as empty.  Write another query (queries[9]) to `update' the table to set it appropriately.
queries[8] = """
alter table IndividualMedals add country_id char(3);
"""

queries[9] = """
update IndividualMedals im
set country_id = (select country_id
                  from players p
                  where p.player_id = im.player_id);
"""

### 10. Which country had the largest percentage of players (who won a medal of course) whose names started with a vowel ?
### Output Column: Country Name
queries[10] = """
with temp as (
    select c1.country_id, cast(c2.num_players as float)/c1.num_players as ratio
    from (select country_id, count(player_id) as num_players from players group by country_id) c1, 
         (select country_id, count(player_id) as num_players from players where substr(name, 1, 1) in  ('A', 'E', 'O', 'I', 'U') group by country_id) c2
    where c1.country_id = c2.country_id
)
select c.name 
from temp t, countries c 
where ratio = (select max(ratio) from temp) and t.country_id = c.country_id
"""

### 11. Find all athletes who won at least one of each medal (GOLD, SILVER and BRONZE) at a single Olympics. 
### Output Columns: player_name, olympic_id
### Order by: player_name

queries[11] = """
    (select players.name, olympic_id 
     from events, results, players 
     where players.player_id = results.player_id and events.event_id = results.event_id and medal like '%GOLD%')
    intersect
    (select players.name, olympic_id 
     from events, results, players 
     where players.player_id = results.player_id and events.event_id = results.event_id and medal like '%SILVER%')
    intersect
    (select players.name, olympic_id 
     from events, results, players 
     where players.player_id = results.player_id and events.event_id = results.event_id and medal like '%BRONZE%')
"""

### 12. In the individual events where the result was noted in seconds, write a query to 
### find which Gold Medal winning player had the largest margin of 
### victory over the Silver medal. Be careful -- there are events where there was no Silver 
### medal, but multiple Gold medals were awarded. You might want to 
### create a temporary table using WITH ``temp(event_id, gold_player_id, gold_result, silver_result)''.
### Output columns: player_name

queries[12] = """
with temp as (
    select r1.event_id, r1.player_id as gold_player_id, r1.result as gold_result, 
                                        r2.result as silver_result, r2.result - r1.result as diff
    from IndividualMedals r1, IndividualMedals r2, events e
    where r1.event_id = r2.event_id and r1.medal = 'GOLD' and r2.medal = 'SILVER' 
                                    and e.event_id = r1.event_id and e.result_noted_in = 'seconds'
)
select e.name, p.name
from temp t, events e, players p
where t.diff = (select max(diff) from temp) and e.event_id = t.event_id and p.player_id = t.gold_player_id
"""

### 13. Write a query to find for all countries, the total number of medals it won and the `rank' of the country 
### by that metric (i.e., the country with the largest number of medals is ranked 1, etc). If two countries tie, 
### they get the same rank, and the next rank is skipped.
### Output columns: country_name, num_medals, rank
### Output order: ascending by rank
### HINT: There is a special operator in SQL to help with this.

queries[13] = """
with temp1 as (
    (select p.country_id, im.medal
     from IndividualMedals im, players p
     where  p.player_id = im.player_id)
    union ALL
    (select tm.country_id, tm.medal
     from TeamMedals tm
    )
),
temp2 as (
    select country_id, count(*) as all_count
    from temp1
    group by country_id
)
select countries.name, t1.all_count, (select count(*) from temp2 t2 where t1.all_count < t2.all_count) + 1 as rank
from temp2 t1, countries
where t1.country_id = countries.country_id
order by rank asc;
"""
