# coding: utf8
try:
    from django.db import connection, transaction 
except:
    import MySQLdb
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
            self.database = MySQLdb.connect(host = "",
                                 user = "",
                                 passwd = "",
                                 db = "",
                                 use_unicode = True,
                                 charset = 'utf8')
            self.cursor = self.database.cursor()
    def execute(self, query):
        """
         Returns a list containing the rows fatched from the query.

        @param string query : 
        @return  :
        @author
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self):
        try:
            transaction.commit_unless_managed() #this is how you commit using django
        except:
            self.database.commit()

    def find(self, queryStart, parameters):
        complements = []
        for key in parameters:
            if isinstance(parameters[key],int): 
                complements.append(key + ' = ' + str(parameters[key]))
            elif isinstance(parameters[key],str):
                if key.split('_')[1] == 'equal':
                    complements.append(key.split('_')[0] + ' = "' + parameters[key] + '"')
                elif key.split('_')[1] == 'like':
                    complements.append(key.split('_')[0] + ' RLIKE "' + parameters[key] + '"')
        if len(complements) > 0:
            query = queryStart + ' WHERE '
            query = query + ' AND '.join(complements)
        else:
            query = queryStart
        return self.execute(query)
