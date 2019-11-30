#!/usr/bin/python
# 2019  Jim Harris <ja_harris@rogers.com>
"""database.py - do database things"""

import psycopg2
import configparser

Configfile = '/home/jim/conf/postgres.conf'
Verbose = False

def pverbose(comment):
    '''verbose output'''
    if Verbose:
        print(comment)

class table_config:
    '''sql table definition

    a list, and a dictionary
    '''
    def __init__(self):
        self.fields = []
        self.field_defs = {}

class db_connect:
    '''a database connection'''
    def __init__(self):
        '''connect to the database'''
        config = configparser.ConfigParser()
        config.read(Configfile)
        database = config['debcat']['database']
        user = config['debcat']['user']
        password = config['debcat']['password']
        host = config['debcat']['host']
        port = config['debcat']['port']
        self.conn = psycopg2.connect(
                database=database, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def create(self, tableconfig, table_name='moose'):
        ''' create table public.moose for DB_fields'''
        statement = ["CREATE TABLE public.{} (".format(table_name),]
        assert type(tableconfig) == type(table_config())
        for key in tableconfig.fields:
            statement.append("  {:20} {},".format(key, tableconfig.field_defs[key]))
        statement.append("  {:20} {}".format('{}_id'.format(table_name), 'serial NOT NULL PRIMARY KEY'))
        statement.append(")")
        statement.append("WITH (OIDS=FALSE);")
        statement.append("ALTER TABLE public.{} OWNER TO jim;".format(table_name))
        print('\n'.join(statement))
        create_statement = '\n'.join(statement)
        self.cur.execute(create_statement)
        self.conn.commit()

    def drop(self, table_name='moose'):
        '''drop table public.moose (or whichever)'''
        statement = "DROP TABLE IF EXISTS public.{};".format(table_name)
        pverbose(statement)
        self.cur.execute(statement)
        self.conn.commit()


    def insert(self, songrecord, tableconfig, table_name='moose'):
        '''write song record to table public.moose'''
        #assert type(songrecord) == type(song_record())
        assert type(tableconfig) == type(table_config())
        insert = "INSERT INTO public.{} (\n".format(table_name)
        field_names = []
        field_values = []
        values = ''
        for key in songrecord.tags.keys():
            field_names.append(key)
            if tableconfig.field_defs[key] == 'integer':
                #print("{} is an integer".format(key))
                if songrecord.tags[key] == '':
                    values = values + "Null, "
                else:
                    values = values + str(songrecord.tags[key]) + ", "
            elif songrecord.tags[key] == '':
                values = values + "Null, "
            else:
                values = values + "'" + str(songrecord.tags[key]).replace("'", "''") + "', "

        names  = ", ".join(field_names)
        values = values[:-2]

        statement = insert + names + "\n) \nVALUES (\n" + values + "\n);"

        pverbose('')
        pverbose(statement)
        pverbose('')
        self.cur.execute(statement)
        self.conn.commit()

    def lookup(self, fields, tableconfig, table_name='moose'):
        '''database lookup on one or more field values

        fields = { field: value, ... }
        '''
        assert type(fields) == type({})
        statement = "SELECT * FROM public.{} WHERE".format(table_name)
        for key in fields.keys():
            pverbose(" -- {:20}: {}".format(key, fields[key]))
            clause = " {} = '{}' AND ".format(key, str(fields[key]).replace("'", "''"))
            statement = statement + clause
        statement = statement[0:-5] + ';'
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

