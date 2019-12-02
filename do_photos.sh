#!/usr/bin/bash


psql -c "SELECT abspath FROM public.photos ORDER BY abspath;" |
    while read abspath
    do
	if [ -f "$abspath" ]
	then
            echo $abspath
	    archive.py -x "$abspath"
	fi
    done
