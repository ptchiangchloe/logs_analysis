# Logs Analysis Project

This is a project is built to discover what kind of articles readers like by querying data from the news data.

## Views for the project

### Most_popular_articles
```
CREATE VIEW most_popular_articles AS
SELECT articles.title, count(log.path) AS num
FROM log, articles WHERE log.path
LIKE '%' || articles.slug  || '%'
GROUP BY articles.title ORDER
LIMIT 3
BY num DESC;
```

### Popular_authors
```
CREATE VIEW popular_authors AS
SELECT authors.name, articles.title FROM authors, articles
WHERE authors.id = articles.author;
```

### Num_of_total
```
CREATE VIEW num_of_total AS
SELECT log.time::date, count(status) AS num
FROM log
GROUP BY log.time::date;
```
### Num_of_error
```
CREATE VIEW num_of_error AS
SELECT log.time::date, count(status) AS num
FROM log
WHERE status != '200 OK'
GROUP BY log.time::date;
```
### Percentage_of_error
```
CREATE VIEW percentage_of_error AS
SELECT num_of_error.time, round(((num_of_error.num::numeric  / num_of_total.num::numeric ) * 100 ), 2) AS percentage
FROM num_of_total, num_of_error
WHERE num_of_error.time = num_of_total.time ;
```


### Prerequisites

This project is only for local development, so you should have a local server service such as VirtualBox.

### Installing

Install the Virtual Machine steps:

https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0

To load the news data:

Use this command in the vagrant directory

```
psql -d news -f newsdata.sql
```

To print analysis result:
```
python fetch_analysis.py
```
To view analysis result:
```
cat logs_analysis.txt
```

## Built With

* [Python2.7](https://www.python.org/) - The language used
* [PostgreSQL](https://www.postgresql.org/) - Dependency Management
* [psycopg2](http://initd.org/psycopg/) - The PostgreSQL adapter for the Python programming language

## Authors

* **Hanyu Jiang** - *Initial work*
