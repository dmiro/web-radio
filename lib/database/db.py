import sqlite3
from contextlib import contextmanager


PATH_RADIO_DB = './data/radio.db'


def as_list(item):
    """Wrap 'item' in a list if it isn't already one.
    """
    if isinstance(item, (str, unicode)):
        return [item]
    return item

@contextmanager
def as_connection(db):
    if isinstance(db, (str, unicode)):
        with sqlite3.connect(db) as conn:
            yield conn
    else:
        yield db

def execute_sql(conn, sqlcmds):
    """
    conn: Database connection that conforms to the Python DB API.
    sqlcmds: List of SQL statements, to be executed in order.
    """
    curs = conn.cursor()
    for cmd in sqlcmds:
        curs.execute(cmd)
    return curs.fetchall()

def query(sqlcmd, database):
    with as_connection(database) as connection:
        return execute_sql(connection, as_list(sqlcmd))

def get_tags():
    return query('select TagName, StationCount from TagCache order by TagName;', PATH_RADIO_DB)

def get_stations_by_tag(tag):
    return query("select Name, Url, Bitrate from Station where Tags like '%{0}%';".format(tag), PATH_RADIO_DB)

def get_countries():
    return query("select Country, count(*) as N from Station where Country <> '' group by lower(Country) order by Country;", PATH_RADIO_DB)

def get_stations_by_country(country):
    return query("select Name, Url, Bitrate from Station where lower(Country) like '%{0}%';".format(country.lower()), PATH_RADIO_DB)

def get_languages():
    return query("select Language, count(*) as N from Station where Language <> '' group by lower(Language) order by Language;", PATH_RADIO_DB)

def get_stations_by_language(language):
    return query("select Name, Url, Bitrate from Station where lower(Language) like '%{0}%';".format(language.lower()), PATH_RADIO_DB)

def get_stations_by_text(text):
    return query("select Name, Url, Bitrate from Station where lower(Name) like '%{0}%';".format(text.lower()), PATH_RADIO_DB)

def get_station_by_url(url):
    result = query("select Name, Url, Bitrate from Station where Url = '{0}';".format(url), PATH_RADIO_DB)
    return result[0] if len(result) > 0 else None
