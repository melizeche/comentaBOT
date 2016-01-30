#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import json
import requests
import sqlite3

# FROM > TO
FROM = int(1446416)
TO = int(1347790)
# https://graph.facebook.com/comments?id=http://abc.com.py/1447680.html&limit=500&fields=message
MAX_ERRORS=4
# path to sqlite database
DB = "fbcomments.db"

# connect db


def connectDB():
    try:
        conn = sqlite3.connect(DB)
        return conn
    except sqlite3.OperationalError as err:
        print("SQLite: {0}".format(err))
        pass


def createTable():
    conn = connectDB()
    c = conn.cursor()
    try:
        c.execute(
            '''CREATE TABLE comments( id INTEGER PRIMARY KEY AUTOINCREMENT, fb_id text unique, comment text)''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as err:
        print("SQLite: {0}".format(err))
        pass


def getUrls():
    urls = []
    for page_id in list(range(FROM, TO, -1)):
        urls.append(
            "https://graph.facebook.com/comments?id=http://abc.com.py/%s.html&limit=500&fields=message" % page_id)
    return urls

if __name__ == "__main__":
    error_count=0
    if not os.path.isfile(DB):
        createTable()
    urls = getUrls()
    print("URLs a escanear: " + str(len(urls)))
    db_conn = connectDB()
    cursor = db_conn.cursor()
    for i, url in enumerate(urls):
        if error_count>MAX_ERRORS:
            raise SystemExit
        print(str(i) + " - " + url)
        data="{}"
        try:
            data = requests.get(url, timeout=8).text
        except Exception as err:
            error_count += 1
            msg = "RequestURL: {0}\n".format(err)
            with open('error.log', 'a') as f:
                f.write(url + ": " + str(msg))
        comments = json.loads(data)
        if 'data' in comments:
            for entry in comments['data']:
                comment = entry['message']
                fbid = entry['id']
                cursor.execute('''INSERT OR IGNORE INTO comments(fb_id, comment) 
                    VALUES(?,?)''', (fbid, comment))
            db_conn.commit()
        else:
            with open('error.log', 'a') as f:
                f.write(url + ": " + str(comments) + "\n")
    db_conn.close()
