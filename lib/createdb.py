#!/usr/bin/env python

import subprocess
import gzip
import os


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


def create_db():

    # init

    print '--init--'

    # creating database backup

    if os.path.exists(DATABASE_FILE):
        print 'creating database backup'
        os.rename(DATABASE_FILE, DATABASE_BAK_FILE)

    # download radio-browser database

    print 'download radio-browser database'
    subprocess.call(['curl', 'http://www.radio-browser.info/backups/latest.sql.gz', '--output', os.path.realpath(LATEST_GZ_FILE)])

    # decompress database

    print 'decompress database'
    inF = gzip.open(LATEST_GZ_FILE, 'rb')
    outF = open(LATEST_FILE, 'wb')
    outF.write( inF.read() )
    inF.close()
    outF.close()

    # convert dump from mysql to sqlite

    print 'convert dump from mysql to sqlite'
    process = subprocess.Popen([os.path.realpath('./lib/mysql2sqlite'), os.path.realpath(LATEST_FILE)], stdout=subprocess.PIPE)
    out, err = process.communicate()
    outF = open(LATEST_SQLITE_FILE, 'wb')
    outF.write( out )
    outF.close()

    # create and populate database

    print 'create and populate database'
    myinput = open(LATEST_SQLITE_FILE)
    p = subprocess.Popen(['sqlite3', DATABASE_FILE], stdin=myinput)
    p.wait()

    # remove files

    print 'removing files'
    if os.path.exists(LATEST_GZ_FILE): os.remove(LATEST_GZ_FILE)
    if os.path.exists(LATEST_FILE): os.remove(LATEST_FILE)
    if os.path.exists(LATEST_SQLITE_FILE): os.remove(LATEST_SQLITE_FILE)

    # end

    print '--end--'


def check_db():

    # update database if import date is older than 1 day
    if os.path.isfile(DATABASE_FILE):
        pass
    # import database
    else:
        create_db()

#
# main
#

if __name__ == '__main__':
    create_db('.')


    








