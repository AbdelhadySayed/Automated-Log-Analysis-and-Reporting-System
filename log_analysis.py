#!/usr/bin/env python2.7

import psycopg2


DBNAME = "news"


def get_answer(statement):
    """Return some data from the 'database', based on statement."""

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(statement)
    answer = c.fetchall()
    db.close()
    return answer


output_file = open('log analysis report', 'w')
# The title of the report.
output_file.write("\n\n\nLog Analysis Report \n\n")


def popular_articles():
    """write the three top viewed articles
    and their number of views in .txt file. """

    top_articles = get_answer(
        "select title, count (*) as views from articles"
        + " join log on right (log.path, -9) = articles.slug"
        + " group by title order by views desc limit 3;")

    output_file.write("\n1. The most popular three articles of all time:-\n\n")
    for item in top_articles:
        output_file.write("-- " + item[0] +
                          "   >>> " + str(item[1]) + " Views.\n")


def popular_authors():
    """write the two top popular authors
    and their number of views in .txt file."""

    top_authors = get_answer(
        "select authors.name, count (*) as views from articles "
        + "join log on right (log.path, -9) = articles.slug join authors "
        + "on authors.id = articles.author group by name order "
        + "by views desc;")
    output_file.write(
        "\n\n\n2. The most popular article authors of all time:-\n\n")
    for item in top_authors:
        output_file.write("-- " + item[0] +
                          "   >>> " + str(item[1]) + " Views.\n")


def high_error_day():
    """write the date that has error percent exceed 1%
    from HTTP requests .txt file."""

    high_error_day = get_answer(
        "select date, error_percent from errorpercent "
        + "where error_percent > 1.0;")
    output_file.write(
        "\n\n\n3. The day that has more than 1% "
        + "of requests lead to errors:-\n\n")
    for item in high_error_day:
        output_file.write(
            "-- " + item[0] + "   >>> "
            + str(round(item[1], 2)) + "% Errors.\n")


popular_articles()
popular_authors()
high_error_day()
