import sqlite3
from enum import Enum
from datetime import datetime

db_name = 'file:quartet_session_database?mode=memory&cache=shared'
table = 'SESSION'


class SessionState(Enum):
    STARTED = 'STARTED'
    COMPLETE = 'COMPLETE'
    STOPPED = 'STOPPED'


def get_session(database_name: str = None, table_name: str = None):
    """
    If there is a running session this will return it.
    :return: A tuple of lot, expiry, state and start_date or None.
    """
    database_name = database_name or db_name
    table_name = table_name or table
    db = sqlite3.connect(database_name)
    cursor = db.execute('SELECT * from %s LIMIT 1' % table_name)
    return cursor.fetchone()

def start_session(lot: str, expiry, state=SessionState.STARTED.value,
                  database_name: str = None, table_name: str = None):
    database_name = database_name or db_name
    table_name = table_name or table
    db = sqlite3.connect(database_name)
    db.execute('INSERT into %s (lot, expiry, state, start_date) '
               'VALUES (?, ?, ?, ?)' % table_name,
               (lot, expiry, state, datetime.now().isoformat()))
    db.close()

def stop_session(lot, database_name = None, table_name = None):
    """
    Updates the session record by stopping it.
    :param lot: The lot used to look up the record.
    :param database_name: The name of the database
    :param table_name: The name of the table
    :return: None
    """




def create_session_db(database_name: str = None, table_name: str = None):
    """
    Creates the in-memory session database.
    :return: None
    """
    database_name = database_name or db_name
    db = sqlite3.connect(database_name)
    table_name = table_name or table
    db.execute('CREATE table if not exists %s '
               '('
               'lot text, '
               'expiry text, '
               'state text, '
               'start_date text'
               ')' % table_name)
    db.close()
