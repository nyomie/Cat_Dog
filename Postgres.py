# This will be the file that has our Postgres class

import logging
import psycopg2


class Postgres:
    """
    This class will provide our setup, connection, cursor, and SQL Commands
    """
    def __init__(self, database=None, user=None, password=None):
        self.database = database
        self.user = user
        self.password = password
        self._ready = False
        self.cursor = None
        self.conn = None
        logging.basicConfig(filename="catdog.log",
                            level=logging.DEBUG,
                            format='%(asctime)s, %(levelname)s, %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def connect(self):
        """
        This method handles connecting to the database and obtaining a cursor
        """
        try:
            self.conn = psycopg2.connect(dbname=self.database,
                                         user=self.user,
                                         password=self.password)
            self.cursor = self.conn.cursor()
            self._ready = True
        except Exception as e:
            logging.error(e)
            self._ready = False

        return self._ready

    def execute_command(self, command=None):
        """
        This method executes and commits the SQL statements.
        It takes as an input a command (string).
        If it fails to write, rollback
        """
        if not self._ready:
            logging.info("Connection not ready.")
            return None

        logging.info(command)

        try:
            self.cursor.execute(command)
            self.conn.commit()
            return True
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            return False

    def create_table(self, table_name=None, table_list=[]):
        """
        This method can be used to create a table in the database.
        It takes an input of table_name (string) and table_list (list)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False
        if len(table_list) == 0:
            return False

        table_string = "create table " + table_name + "("

        for column, type in table_list:
            table_string += "%s %s," % (column, type)
        table_string = table_string[:-1]
        table_string += ");"

        return self.execute_command(table_string)

    def insert_data(self, table_name=None, values=[]):
        """
        This method will insert 1 row of data into the database.
        It has inputs of table_name (string) and values (list)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False
        if len(values) == 0:
            return False

        command_string = "insert into " + table_name + " ("

        for column in values[0]:
            command_string += column + ","
        command_string = command_string[:-1]
        command_string += ") values ("

        for data in values[1]:
            if type(data).__name__ == 'str':
                command_string += "\'%s\'," % data
            elif type(data).__name__ == 'float':
                command_string += "%f," % data
            elif type(data).__name__ == 'int':
                command_string += "%d," % data
            else:
                command_string += "\'%s\'," % str(data)
        command_string = command_string[:-1]
        command_string += ");"

        return self.execute_command(command_string)

    def query_all_data(self, table_name=None):
        """
        This method will return all data in the table.
        It takes input of table_name (string)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False

        command_string = "select * from " + table_name
        self.execute_command(command_string)

        try:
            return self.cursor.fetchall()
        except Exception as e:
            logging.info("No data found: " + str(e))
            return None

    def query_specific_data(self, table_name=None, query_data=None):
        """
        This method will return specific data in the table.
        It takes input of table_name (string) and query_data (string)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False
        if query_data is None:
            return False

        command_string = "select * from " + table_name + " where " + query_data
        self.execute_command(command_string)

        try:
            return self.cursor.fetchall()
        except Exception as e:
            logging.info("No specific data found: " + str(e))
            return None

    def aggregate_result(self, table_name=None, column_name=None):
        """
        This method will count the number of rows that matches a specified criteria.
        It takes input of table_name (string) and column (string)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False
        if column_name is None:
            return False

        command_string = "select " + column_name + ", count(*) from " + table_name + " group by " + column_name + \
                         " order by count (*) desc"
        self.execute_command(command_string)

        try:
            return self.cursor.fetchall()
        except Exception as e:
            logging.info("No aggregated result found: " + str(e))
            return None