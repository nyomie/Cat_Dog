# This will be our main web codes

import os
import flask
import jinja2
import sys
from flask_restful import Api
import Postgres
import CheckValid
import Chart
import CatDogAPI


"""
collection of global variables that we need
"""


app = flask.Flask(__name__, static_url_path='/static')
api = Api(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
env = jinja2.Environment(
    loader=jinja2.PackageLoader(__name__,
                                'templates'))
app.secret_key = 'Th1sisRAnd0m!'
database = 'postgres'                              # Your postgres database name
user = 'postgres'                                  # Your postgres user name
password = os.getenv('PASSWORD')                   # Set your password in environment variable named 'PASSWORD'
table_name = "Poll_Cat_Dog"

"""
Connecting to database and creating table to store respond
"""


db = Postgres.Postgres(database=database,
                       user=user,
                       password=password)
if not db.connect():
    sys.exit(1)

# Only run these lines when it runs on your local computer first time:
# db.create_table(table_name=table_name, table_list=[("email", "text"), ("choice", "text")])


"""
HTML PAGE
"""


@app.route('/', methods=['GET', 'POST'])
def front_page():
    """
    Front page
    """
    if flask.request.method == 'POST':
        html = display_result()
    else:
        html = cat_or_dog()
    return html


def cat_or_dog():
    """
    Show the form that includes the email and the cat or dog radio button
    """
    template = env.get_template('cat_or_dog.html')
    html =  template.render()
    return html


def display_result():
    """
    Display stock data
    """
    email = flask.request.form['email'].upper()
    choice = flask.request.form['cat_or_dog']

    if not CheckValid.is_email(email):
        return invalid_user()

    if CheckValid.is_new_user(email):
        db.insert_data(table_name=table_name, values=[('EMAIL','CHOICE'),(email,choice)])
        error = ''
    else:
        error = 'You already did this poll. Come back when we have new poll. <br><br>'

    data = db.aggregate_result(table_name=table_name, column_name='CHOICE')
    Chart.Chart(data)
    template = env.get_template('display_result.html')
    html = template.render(error_if_any=error, DATA=data, chart = 'static/chart.png')
    return html



@app.errorhandler(404)
def page_not_found(error):
    """
    Basic 404 error handler page
    """
    template = env.get_template('error.html')
    html = template.render(ERROR="404", message="Page Not Found")
    return html


def invalid_user():
    """
    Invalid email error handler page
    """
    template = env.get_template('error.html')
    html = template.render(ERROR="401", message="Invalid email")
    return html

api.add_resource(CatDogAPI.Aggregate_Result, '/poll_result')
api.add_resource(CatDogAPI.List_Vote,"/list_vote/<string:choice>")


if __name__ == '__main__':
    """
    Application entry point
    """
    use_debugger = True
    app.run(debug=True)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, ' \
                                        'post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
