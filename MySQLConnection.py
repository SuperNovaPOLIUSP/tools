# coding: utf8
try:
    from django.db import connections, transaction 
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
            self.database = connections['default']
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
        self.database.commit()


