#!/usr/bin/env python2
import psycopg2

def connect(database_name):
    try:
        conn = psycopg2.connect("dbname={}".format(database_name))
        cur = conn.cursor()
        return conn, cur
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)
        raise e

def get_query_result(query):
    conn, cur = connect('news')
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

def print_top_articles():
    rows = get_query_result("""SELECT articles.title, count(log.path) as num
                                FROM log, articles
                                where log.path LIKE '%' || articles.slug  || '%'
                                GROUP BY articles.title ORDER
                                BY num DESC
                                LIMIT 3;""")

    print 'What are the most popular three articles of all time? '

    for i in range(len(rows)):
        print("{}: '{}' -- {} views".format(i+1, rows[i][0], rows[i][1]))

def print_top_authors():
    rows = get_query_result("""SELECT popular_authors.name, sum(most_popular_articles.num::numeric) as num
                FROM popular_authors, most_popular_articles
                WHERE popular_authors.title = most_popular_articles.title AND popular_authors.name != 'Anonymous Contributor'
                GROUP BY popular_authors.name
                ORDER BY num DESC;""")

    print 'Who are the most popular article authors of all time?'

    for i in range(len(rows)):
        print("{}: '{}' -- {} views").format(i+1, rows[i][0], rows[i][1])

def print_top_error_days():
    rows = get_query_result("""select time as date, (percentage || '%')as error_percentage
                from percentage_of_error
                where percentage > 1;""")

    print 'Which days did more than 1% of requests lead to errors?'

    for i in range(len(rows)):
        print("{} -- {} errors").format(rows[i][0], rows[i][1])

if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
