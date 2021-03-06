#!/usr/bin/env python

import gzip
import os
import subprocess
from datetime import datetime, timedelta
from shutil import copy2

from lib.helpers.execute import execute

"""
create database from repository radio-browser.info in sqlite format

prerequisites:

(1) install sqlite3 (client) 
    > sudo apt-get install sqlite3
(2) copy mysql2sqlite script from github
    https://github.com/dumblob/mysql2sqlite

"""


DATABASE_FILE = './data/radio.db'
DATABASE_BAK_FILE = './data/radio.db.bak'
LATEST_GZ_FILE = './data/latest.sql.gz'
LATEST_FILE = './data/latest.sql'
LATEST_SQLITE_FILE = './data/latest.sqlite'
MYSQL2SQLITE_FILE = './lib/database/mysql2sqlite'

def create_db():

    # init

    print '--init--'

    try:

        # creating database backup

        if os.path.exists(DATABASE_FILE):
            print 'creating database backup'
            os.rename(DATABASE_FILE, DATABASE_BAK_FILE)

        # download radio-browser database

        print 'download radio-browser database'
        execute(['curl', 'http://www.radio-browser.info/backups/latest.sql.gz', '--output', os.path.realpath(LATEST_GZ_FILE)], timeout=40)

        # decompress database

        print 'decompress database'
        inF = gzip.open(LATEST_GZ_FILE, 'rb')
        outF = open(LATEST_FILE, 'wb')
        outF.write(inF.read())
        inF.close()
        outF.close()

        # convert dump from mysql to sqlite

        print 'convert dump from mysql to sqlite'
        process = subprocess.Popen([os.path.realpath(MYSQL2SQLITE_FILE), os.path.realpath(LATEST_FILE)], stdout=subprocess.PIPE)
        out, err = process.communicate()
        outF = open(LATEST_SQLITE_FILE, 'wb')
        outF.write(out)
        outF.close()

        # create and populate database

        print 'create and populate database'
        myinput = open(LATEST_SQLITE_FILE)
        p = subprocess.Popen(['sqlite3', DATABASE_FILE], stdin=myinput)
        p.wait()

    except Exception as ex:

        # recovering database backup

        print "exception!", ex
        if os.path.exists(DATABASE_BAK_FILE):
            print 'recovering database backup'
            copy2(DATABASE_BAK_FILE, DATABASE_FILE) # copy2 preserve original metadata
        else:
            print 'there is no database backup to recover'

    finally:

        # remove files

        print 'removing files'
        if os.path.exists(LATEST_GZ_FILE): os.remove(LATEST_GZ_FILE)
        if os.path.exists(LATEST_FILE): os.remove(LATEST_FILE)
        if os.path.exists(LATEST_SQLITE_FILE): os.remove(LATEST_SQLITE_FILE)

    # end

    print '--end--'


def check_db():

    # if date file is older than 1 day then update database
    if os.path.isfile(DATABASE_FILE):
        timefile = datetime.fromtimestamp(os.path.getmtime(DATABASE_FILE))
        yesterday = datetime.today() - timedelta(days=1)
        if timefile < yesterday:
            create_db()

    # import database because does not exist
    else:
        create_db()

#
# main
#

if __name__ == '__main__':
    create_db()


    








