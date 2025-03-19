
# Log Analysis

It makes a log analysis of a newspaper website.
when it is executed it created a .txt file with **the most popular
articles and authors** based in views in the website 
and also **the date of the day of requests errors > 1%**.


## Installation required

- Linux-based virtual machine(VM)
- python 2.7


## Views created

1. totalstatus
```
create view totalstatus as select CAST ( log.time AS DATE) as date, 
count(*) as num from log group by date;
```

2. errorstatus
```
create view errorstatus as select CAST ( log.time AS DATE) as date, 
count(*) as num_error from log where status = '404 NOT FOUND' 
group by date order by date;

```

3. errorpercent
```
create view errorpercent as select TO_CHAR(totalstatus.date, 'dd Month yyyy') as date, 
CAST(errorstatus.num_error as FLOAT)/totalstatus.num * 100 as error_percent 
from totalstatus join errorstatus on totalstatus.date = errorstatus.date
order by totalstatus.date;

```


## SQL queries used

```
select title, count (*) as views from articles join log on right (log.path, -9) = articles.slug
group by title order by views desc limit 3;

```

```
select authors.name, count (*) as views from articles join log 
on right (log.path, -9) = articles.slug join authors on authors.id = articles.author 
group by name order by views desc;

```

```
select date, error_percent from errorpercent where error_percent > 1.0;

```


## Methods

- `get_answer` allow to execute statement on the database `news`.

- `popular_articles` uses `get_answer` to get 
   the top poupular articles written in the output file in an ordered way.

- `popular_authors` uses `get_answer` to get 
   the poupular authors written in the output file in an ordered way.

- `high_error_day` uses `get_answer` to get the date of the day
   that has the percent of HTTP requests errors > 1%.

