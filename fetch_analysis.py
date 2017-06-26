import psycopg2

conn = psycopg2.connect(database='news')

cur = conn.cursor()

cur.execute("""SELECT articles.title, count(log.path) as num
            FROM log, articles
            where log.path LIKE '%' || articles.slug  || '%'
            GROUP BY articles.title ORDER
            BY num DESC
            LIMIT 3;""")

rows = cur.fetchall()

print 'What are the most popular three articles of all time? '

for i in range(len(rows)):
    print("{}: '{}' -- {} views".format(i+1, rows[i][0], rows[i][1]))

cur = conn.cursor()

cur.execute("""SELECT popular_authors.name, sum(most_popular_articles.num::numeric) as num
            FROM popular_authors, most_popular_articles
            WHERE popular_authors.title = most_popular_articles.title
            GROUP BY popular_authors.name
            ORDER BY num DESC;""")

rows = cur.fetchall()

print 'Who are the most popular article authors of all time?'

for i in range(len(rows)):
    print("{}: '{}' -- {} views").format(i+1, rows[i][0], rows[i][1])

# for i in range(len(rows)):

cur = conn.cursor()

cur.execute("""select time as date, (percentage || '%')as error_percentage
            from percentage_of_error
            where percentage > 1;""")

rows = cur.fetchall()

print 'Which days did more than 1% of requests lead to errors?'

for i in range(len(rows)):
    print("{} -- {} errors").format(rows[i][0], rows[i][1])

conn.commit()

cur.close()
conn.close()
