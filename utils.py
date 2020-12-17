
"""Where all the utility functions live helper functions"""
import datetime
from dateutil.parser import parse
import hashlib
import requests


def hash_pwd(password):
    """function to hash user's password"""
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_pwd(password, hash):
    """check if password and hash match"""
    if hash_pwd(password) == hash:
        return True
    return False


def time_date():
    """Get current date ex: Wednesday, October 14"""
    today = datetime.date.today()
    one_week_timedelta = datetime.timedelta(days=6)
    sunday = None

    if today.isoweekday() != 7:
        sunday = today - datetime.timedelta(days=today.isoweekday())
    else:
        sunday = today

    saturday = sunday + one_week_timedelta

    return today, str(sunday), str(saturday)
