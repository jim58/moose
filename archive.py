#!/usr/bin/python
'''
    archive.py - archive a picture file

'''

import os
import sys
import time
import re
import psycopg2
import string
import argparse
import datetime
import shutil

from PIL import Image
from PIL.ExifTags import TAGS

rootdir = '/mnt/Local/photosDB'


parser = argparse.ArgumentParser()
parser.add_argument('infile', help='name of file to add to pictures table')
parser.add_argument('-q', '--quiet', action="store_true", help='no output')
parser.add_argument('-v', '--verbose', action="store_true", help='verbose output')
parser.add_argument('-x', '--execute', action="store_true", help='copy file to data store')
args = parser.parse_args()

if args.verbose:
    args.quiet = False

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
    if args.verbose:
        print("  ... no exif data")
    exit(2)


value = {}
myTags = [
    'DateTime', 'DateTimeOriginal', 'DateTimeDigitized',
    'ExifImageWidth', 'ExifImageHeight', 'ImageWidth', 'ImageLength',
    'Make', 'Model', 'Software' ]

for key in myTags:
    value[key] = ''

if args.verbose:
    print("{:20} = {}".format('Filename', infile))

for (k,v) in items:
    keyname = TAGS.get(k)
    if keyname in myTags:
        value[keyname] = v
        if args.verbose:
            print("{:20} = {}".format(keyname, value[keyname]))


if value['DateTime']:
    ymd = value['DateTime'].split(" ")[0]
elif value['DateTimeOriginal']:
    ymd = value['DateTimeOriginal'].split(" ")[0]
elif value['DateTimeDigitized']:
    ymd = value['DateTimeDigitized'].split(" ")[0]
else:
    ymd = filetime.strftime("%Y-%m-%d")

ymd = ymd.replace(":", "-")

model = value['Model']
if model:
    model = model.replace(' ', '_').replace('/', '_')
else:
    model = "unknown"

year = ymd[0:4]
month = ymd[0:7]

targetdir = "{}/{}/{}/{}/{}".format(rootdir, model, year, month, ymd)
destination = "{}/{}/{}/{}/{}/{}".format(rootdir, model, year, month, ymd, filename)

if args.verbose:
    print('os.mkdir("{}")'.format(targetdir))
    print('copy to "{}"'.format(destination))

if not args.execute:
    exit(0)

if args.verbose:
    print("executing copy")

if not os.path.exists(targetdir):
    os.makedirs(targetdir)

if os.path.exists(destination):
    if not args.quiet:
        print(" ... file already exists ({})".format(destination))
    exit(1)
else:
    shutil.copy2(abspath, destination)
    if not args.quiet:
        print(" ... file inserted")

