#! /usr/bin/env python3


def send(text):
    print(text)
    quit()


def check(json_file):
    data = json.load(open(json_file))
    return [obj for obj in data if obj.keys() == {'cfilm': 0, 'cmedia': 0}.keys()]


def update(data):
    conn = sqlite3.connect("new_movies.db") if os.path.exists("new_movies.db") else send("No file 'new_movies.db'")
    c = conn.cursor()
    for val in data:
        c.execute("UPDATE movies SET cmedia=:cmedia WHERE cfilm=:cfilm", val)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import os
    import sys
    import sqlite3
    import json
    import pandas
    df = pandas.read_json(
        json.dumps(check(sys.argv[1])),
        orient='records'
    ).groupby('cfilm')['cmedia'].apply(
        lambda x: ';'.join(set([str(el) for el in x]))
    )
    new = pandas.DataFrame()
    new['cfilm'] = df.index
    new['cmedia'] = df.values
    new = new.to_dict(orient='records')
    update(new)
