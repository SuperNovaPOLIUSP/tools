# coding: utf8

from _mysql import OperationalError
from django.conf import settings
import os
import time
import MySQLdb
import codecs
    
MAXTRIES = 8  # Maximum number of tries before stop trying to connect
SLEEPTIMER = 5  # Number of seconds to wait before each try
MAXDEPTH = 1  # Maximum depth of the search for the configurations file


class MySQLConnection(object):
    """
    :version: 
    :author: 
    """
    """ ATTRIBUTES
    cursor  (public)
    """
    __singleton = None  # TODO

    def __init__(self):
        """
         When initialized the attribute cursor gets django's MySQL cursor.
        @return  :
        @author
        """
        # reads database connection settings from file
        inputConfiguracoesBD = codecs.open(settings.ARQUIVO_CONF_BD, 'r', 'utf-8')
        tries = 0
        host_name = inputConfiguracoesBD.readline()[:-1]
        user_name = inputConfiguracoesBD.readline()[:-1]
        password = inputConfiguracoesBD.readline()[:-1]
        database_name = inputConfiguracoesBD.readline()[:-1]

        while tries < MAXTRIES:
            try:
                self.database = MySQLdb.connect(host = host_name,
                                                user = user_name,
                                                passwd = password,
                                                db = database_name,
                                                use_unicode = True,                                
                                                charset = 'utf8')
                break
            except OperationalError:
                tries += 1
                print 'Error no: ' + str(tries)
                time.sleep(SLEEPTIMER)

        self.cursor = self.database.cursor()           
        MySQLConnection.__singleton = self 

    def execute(self, query):
        """
         Returns a list containing the rows fetched from the query.

        @param string query : 
        @return  :
        @author
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self):
        self.database.commit()

    def find(self, queryStart, parameters, queryEnd = ''):
        complements = []
        for key in parameters:
            if parameters[key] == None:
                complements.append(key.split('_')[0] + ' is null') #Even if there is no _ this will work
            elif isinstance(parameters[key], (int, long)): 
                complements.append(key + ' = ' + str(parameters[key]))
            elif isinstance(parameters[key], (str, unicode)):
                if key.split('_')[1] == 'equal':
                    complements.append(key.split('_')[0] + ' = "' + parameters[key] + '"')
                elif key.split('_')[1] == 'like':
                    complements.append(key.split('_')[0] + ' LIKE "%%' + parameters[key] + '%%"')
            elif isinstance(parameters[key], list):
                #When using multiple terms they are OR
                tempComplements = []
                for parameter in parameters[key]:
                    if parameter == None:
                        tempComplements.append(key.split('_')[0] + ' is null') #Even if there is no _ this will work
                    elif isinstance(parameter, (int, long)): 
                        tempComplements.append(key + ' = ' + str(parameter))
                    elif isinstance(parameter, (str, unicode)):
                        if key.split('_')[1] == 'equal':
                            tempComplements.append(key.split('_')[0] + ' = "' + parameter + '"')
                        elif key.split('_')[1] == 'like':
                            tempComplements.append(key.split('_')[0] + ' LIKE "%%' + parameter + '%%"')
                complements.append('(' + ' OR '.join(tempComplements) + ')')
       
        if len(complements) > 0:
            query = queryStart + ' WHERE '
            query = query + ' AND '.join(complements)
        else:
            query = queryStart
        query = query + queryEnd
        return self.execute(query)
    
    def close(self):
        self.database.close()
        
class MySQLQueryError(Exception):
    """
     Exception reporting an error in the execution of a MySQL query.

    :version:
    :author:
    """
    pass
