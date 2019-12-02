#!/usr/bin/python

import os
import sys
import time
import re
import psycopg2
import string
import argparse
import datetime
import configparser

from PIL import Image
from PIL.ExifTags import TAGS



parser = argparse.ArgumentParser()
parser.add_argument('--nosql', action="store_true", help='do not connect to postgres')
parser.add_argument('-q', '--quiet', action="store_true", help='no output')
parser.add_argument('infile', help='name of file to add to photos table')
args = parser.parse_args()

#print(args)

DB_config_file = '/home/jim/conf/postgres.conf'

infile = args.infile

filename = os.path.basename(infile)
abspath = os.path.abspath(infile)
dirname = os.path.dirname(abspath)

thing = os.stat(abspath)
filesize = thing.st_size
filetime = datetime.datetime.fromtimestamp(int(round(thing.st_mtime)))
if filesize == 0:
    exit(1)

try:
    items = Image.open(abspath)._getexif().items()
except:
    if args.quiet == False:
        print("  ... no exif data")
    exit(21)

if len(items) == 0:
    if args.quiet == False:
        print("  ... no exif data")
    exit(22)
        

value = {}
myTags = [
    'DateTime', 'DateTimeOriginal', 'DateTimeDigitized',
    'ExifImageWidth', 'ExifImageHeight', 'ImageWidth', 'ImageLength',
    'Make', 'Model', 'Software' ]

for key in myTags:
    value[key] = ''

if args.quiet == False:
    print("{:20} = {}".format('Filename', infile))
for (k,v) in items:
    keyname = TAGS.get(k)
    if keyname in myTags:
        value[keyname] = v
        if args.quiet == False:
            print("{:20} = {}".format(keyname, value[keyname]))


im = Image.open(abspath)
width = im.width
height = im.height
if args.quiet == False:
    print()
    print("{:20} = {}".format('width', width))
    print("{:20} = {}".format('height', height))
    print("{:20} = {}".format('filesize', filesize))
    print("{:20} = {}".format('filetime', filetime))


db_config = configparser.ConfigParser()
db_config.read(DB_config_file)
database = db_config['debcat']['database']
user = db_config['debcat']['user']
password = db_config['debcat']['password']
host = db_config['debcat']['host']
port = db_config['debcat']['port']
conn = psycopg2.connect(
        database=database, user=user, password=password, host=host, port=port)
cur = self.conn.cursor()

if args.quiet == False:
    print("connected to postgresql")

statement = "SELECT count(abspath) FROM public.photos WHERE abspath = '{}';".format(abspath.replace("'", "`"))
if args.quiet == False:
    print(statement)

cur.execute(statement)
rows = cur.fetchall()
for row in rows:
    cnt = row[0]
    if args.quiet == False:
        print("database count is {}".format(cnt))
    if cnt > 0:
        exit(3)

if args.nosql:
    if args.quiet == False:
        print(" no sql insertion")
    exit(4)


#print("{:20} = {}".format('ImageWidth', value['ImageWidth']))
#print("{:20} = {}".format('ImageLength', value['ImageLength']))

cur.execute("""
    INSERT INTO public.photos( filename, width, height, filesize, filetime,
        DateTime, DateTimeOriginal, DateTimeDigitized, ExifImageWidth, ExifImageHeight,
        Make, Model, Software, dirname, abspath)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """,
    ( filename.replace("'", "''"), width, height, filesize, filetime,
      value['DateTime'], value['DateTimeOriginal'], value['DateTimeDigitized'],
      value['ExifImageWidth'], value['ExifImageHeight'],
      value['Make'], value['Model'], value['Software'], dirname.replace("'", "`"), abspath.replace("'", "`"))
)
conn.commit()

