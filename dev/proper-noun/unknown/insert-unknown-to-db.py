#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import os, sys, MySQLdb, codecs

''' all global variables here '''

# database parameters
db_params = {'host': 'localhost',
             'user': 'root',
             'passwd': 'root',
             'db': 'bengali_conjugator'}
# list for the words to be inserted
entries = []


''' class defs here '''
class Connection(object):
    ''' Db connection class '''
    def __init__(self):
        self.conn = MySQLdb.connect(host = db_params['host'], user = db_params['user'], passwd = db_params['passwd'], db = db_params['db'])
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET CHARACTER SET utf8')
        
    def close(self):
        self.cursor.close()
        self.conn.close()
        
class DbHelper(object):
    def __init__(self, cursor):
        self.cursor = cursor
    
    def db_contains_word(self, word, table_name, field_name):
        sql = ''' SELECT count(*) as row_count FROM %s where %s = '%s' ''' % (table_name, field_name, word.encode('utf-8'))
        self.cursor.execute(sql)
        row_count, = self.cursor.fetchone()
        if row_count == 0:
            # if not found, return false
            return False
        return True
    
    def insert_word(self, table_name, dix):
        fields = ''
        values = ''
        for k, v in dix.iteritems():
            fields += k + ','
            values += '\'' + v.encode('utf-8') + '\'' + ','
        fields = '(' + fields[:-1] + ')'
        values = '(' + values[:-1] + ')'
        
        sql = ''' insert into %s %s values %s ''' % (table_name, fields, values)
        print sql
        self.cursor.execute(sql)
        
def read_from_stdin():
    # read entries from stdin
    for word in sys.stdin:
        word = word.strip().decode('utf-8')
        # only insert if unique
        if word not in entries:
            entries.append(word)
    
    # sort the enties
    entries.sort()
    
if __name__ == "__main__":
    try:
        # database connection
        connection = Connection()
        cursor = connection.cursor
        dbHelper = DbHelper(cursor)
        
        read_from_stdin()
        #print entries
        
        for word in entries:
            if not dbHelper.db_contains_word(word, 'proper_noun_source_freq', 'lemma'):
                print 'Inserting', word
                dbHelper.insert_word('proper_noun_source_freq', {'lemma': word,
                                                                 'animacy': '0',
                                                                 'freq': '0',
                                                                 'gender': '0',
                                                                 'number': '0',
                                                                 'nptag': '0',
                                                                 'old': '0'})
                
            else:
                print word, 'is already in Db, not inserting'
        connection.close() 
    except MySQLdb.Error, e:
        print 'ERROR: ', e
        sys.exit (1)
