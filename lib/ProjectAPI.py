# This file will contain the code to build the API for this application

import sys
from flask_restful import Resource
from lib import Postgres
import os


database = 'postgres'                              # Your postgres database name
user = 'postgres'                                  # Your postgres user name
password = os.getenv('PASSWORD')                   # Set your password in environment variable
table_name = "Poll_Cat_Dog"

db = Postgres.Postgres(database=database,
                       user=user,
                       password=password)


class Aggregate_Result(Resource):
    def get(self):
        # Connect to databse
        if not db.connect():
            sys.exit(1)
        # Perform query and return JSON data
        data = db.aggregate_result(table_name=table_name, column_name='CHOICE')
        return {"results": [{row[0]:row[1]} for row in data]}


class List_Vote(Resource):
    def get(self,choice):
        # Connect to databse
        if not db.connect():
            sys.exit(1)
        # Perform query and return JSON data
        data = db.query_specific_data(table_name=table_name, query_data="choice = '%s'" % choice)
        return {'data': [row[0] for row in data]}