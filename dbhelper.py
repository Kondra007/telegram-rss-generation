# -*- coding: utf-8 -*-

import sqlite3
from config import db_name, number_of_entries
from time import time

def insert(text, date, pid):
    with sqlite3.connect(db_name) as connection:
        connection.execute("INSERT INTO texts(post_text, post_date, post_id) values (?, ?, ?)", (text, date, pid,))
        
 
def get_latest_entries():
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        entries = [dict(ptext=row[0], pdate=row[1], pid=row[2]) for row in cursor.execute("SELECT post_text, post_date, post_id FROM texts ORDER BY id DESC LIMIT ?", (number_of_entries,)).fetchall()]
        return entries
        
def remove_last_entry():
    with sqlite3.connect(db_name) as connection:
        connection.execute("DELETE from texts WHERE id in (SELECT id from texts ORDER BY id DESC LIMIT 1);")    


def remove_old_entries():
    """
    Removes the oldest entries except the number set in config
    """
    with sqlite3.connect(db_name) as connection:
        connection.execute("DELETE FROM texts WHERE id IN (SELECT id FROM texts ORDER BY id DESC LIMIT -1 OFFSET ? )",(number_of_entries,))


