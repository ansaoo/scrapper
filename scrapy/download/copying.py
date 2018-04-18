#!/usr/bin/env python3


def copy(limit='1989'):
    conn = sqlite3.connect('recentMovies.db')
    c = conn.cursor()
    des = sqlite3.connect('new_movies.db')
    dest_cursor = des.cursor()
    c.execute("select title,date,genre,synopsis,trailer,rate from movies")
    purchases = [parse(doc) for doc in c.fetchall() if parse_date(doc[1]) < parser.parse(limit)]
    dest_cursor.executemany(
        "INSERT INTO movies (title,date,genre,synopsis,cfilm,cmedia) VALUES (?,?,?,?,?,?)"
        , purchases)
    des.commit()
    des.close()
    conn.close()


def parse(doc):
    regex = '(.*)cmedia=(?P<cmedia>[0-9]*)&cfilm=(?P<cfilm>[0-9]*).html'
    res = re.match(regex, doc[4])
    return (doc[0],
            parse_date(doc[1], to_str=True),
            doc[2].replace(',', ';'),
            doc[3],
            res.groupdict()['cfilm'] if res else '',
            res.groupdict()['cmedia'] if res else '')


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
    import re
    import sqlite3
    from dateutil import parser
    copy('2017-8-16')
