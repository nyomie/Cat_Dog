# This will be our main web codes

import os
import flask
import jinja2
import sys
import Postgres
import CheckValid


"""
collection of global variables that we need
"""


app = flask.Flask(__name__)
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

db.create_table(table_name=table_name, table_list=[("EMAIL", "text"), ("CHOICE", "text")])


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
    else:
        return not_new_user_error()

    data = db.aggregate_result(table_name=table_name, column_name='CHOICE')
    template = env.get_template('display_result.html')
    html = template.render(DATA=data)
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


def not_new_user_error():
    """
    Not new user error handler page
    """
    template = env.get_template('error.html')
    html = template.render(ERROR="409", message="You already did this poll. Come back when we have new poll.")
    return html


if __name__ == '__main__':
    """
    Application entry point
    """
    use_debugger = True
    app.run(debug=True)