# coding: utf8

try:
    from django.db import connection, transaction 
except:
    import MySQLdb
    import codecs

from types import *

class MySQLConnection(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     

    cursor  (public)

    """



    def __init__(self):
        """
         When initialized the attribute cursor gets django's MySQL cursor.

        @return  :
        @author
        """
        try:
            self.cursor = connection.cursor()
        except:

            # reads database connection settings from file

            inputConfiguracoesBD = codecs.open('./settings.db', 'r', 'utf-8')

            self.database = MySQLdb.connect(host = inputConfiguracoesBD.readline()[:-1],
                                            user = inputConfiguracoesBD.readline()[:-1],
                                            passwd = inputConfiguracoesBD.readline()[:-1],
                                            db = inputConfiguracoesBD.readline()[:-1],
                                            use_unicode = True,                                
                                            charset = 'utf8')

            self.cursor = self.database.cursor()

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
        try:
            transaction.commit_unless_managed() #this is how commits must be done using django
        except:
            self.database.commit()

    def find(self, queryStart, parameters):
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
        return self.execute(query)

class MySQLQueryError(Exception):
    """
     Exception reporting an error in the execution of a MySQL query.

    :version:
    :author:
    """
    pass
