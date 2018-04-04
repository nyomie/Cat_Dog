# This program is checking whether string is valid email address format
import logging

from validate_email import validate_email

from Poll import db, table_name


def is_email(email):
    """
    To see if user inputs existing email address.
    Return True or False
    """
    return validate_email(email, verify="True")


def is_new_user(email):
    """
    To see if we user already register in our database.
    Return True or False
    """
    specific_data = db.query_specific_data(table_name=table_name, query_data="EMAIL = '%s'" % email)

    if specific_data is None:
        logging.info("%s is new user" % email)
        return True
    else:
        logging.error("%s was found" % email)
        return False