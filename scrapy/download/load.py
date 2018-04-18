#!/usr/bin/env python3


def send(text):
    print(text)
    quit()


def check(json_file):
    data = json.load(open(json_file))
    return [obj for obj in data if obj.keys() == data[0].keys()]


def sort(val):
    return (val['titre'],
            parse_date(val['date'], to_str=True),
            ';'.join(val['genre']),
            val['synopsis'],
            ';'.join(val['dirs']),
            ';'.join(val['actors']),
            val['cfilm'],
            avg(val['rate']),
            0.0
            )


def avg(rate_list):
    return sum([float(elem.strip().replace(',', '.'))
                for elem in rate_list]) / len(rate_list) if len(rate_list) != 0 else 0


def load(json_file):
    data = check(json_file)
    conn = sqlite3.connect("new_movies.db") if os.path.exists('new_movies.db') else send("No file 'new_movies.db'")
    c = conn.cursor()
    purchases = []
    for val in data:
        purchases.append(sort(val))
    c.executemany(
        "INSERT INTO movies (title,date,genre,synopsis,dirs,actors,cfilm,rate,estimation) VALUES (?,?,?,?,?,?,?,?,?)",
        purchases)
    conn.commit()
    conn.close()


def parse_date(date, to_str=False):
    mapping = {'janvier': 'january',
               'février': 'february',
               'mars': 'march',
               'avril': 'april',
               'mai': 'may',
               'juin': 'june',
               'juillet': 'july',
               'août': 'august',
               'septembre': 'september',
               'octobre': 'october',
               'novembre': 'november',
               'décembre': 'december'}
    for key in mapping.keys():
        if key in date:
            date = date.replace(key, mapping[key])
    date = parser.parse(date, fuzzy=True)
    return '{0}-{1}-{2}'.format(date.year, date.month, date.day) if to_str else date


if __name__ == "__main__":
    import os
    import sys
    import sqlite3
    import json
    from dateutil import parser
    load(sys.argv[1])
