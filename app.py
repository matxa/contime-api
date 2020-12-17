"""ConTime FastAPI"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import Employee, Employer, Calendar
from pymongo import MongoClient
from typing import Optional
from utils import check_pwd, hash_pwd, time_date
from os import getenv


app = FastAPI(
    title="ConTime API",
    description="ConTime API is the bridge between the backend and the \
frontend of the ConTime Web Application",
    version="v1"
)

"""MongoDB SetUP"""
user_name = getenv('MONGO_USER')
pwd = getenv('MONGO_PWD')
client = MongoClient(f'mongodb+srv://{user_name}:{pwd}@cluster0.qgdv3.\
mongodb.net/ConTime?retryWrites=true&w=majority')
db = client['ConTime']
employer_collection = db['Employer']
employer_collection.create_index("email", unique=True)
employee_collection = db['Employee']
calendar_collection = db['Calendar']


@app.get("/")
def home():
    """Home of ConTime API
    This route redirects to '/docs' route"""
    return RedirectResponse('/docs')


@app.get("/users/{user_type}")
def all_users_by_type(user_type):
    """Get all employers or employees from DataBase"""
    users = None
    users_list = []

    if user_type == 'employer':
        employers = employer_collection.find()
        users = employers
    elif user_type == 'employee':
        employees = employee_collection.find()
        users = employees
    else:
        return {"error": f"[ {user_type} ] is not a valid user type."}

    for user in users:
        del user['_id']
        users_list.append(user)

    return users_list


@app.get("/user/{user_type}")
def get_user_by_type(user_type, email: str, password: str):
    """Get a employer or employee from DataBase"""
    user = None

    if user_type == 'employer':
        employer = employer_collection.find_one({'email': email})
        if employer is None:
            return {"error": f"Invalid email"}
        if check_pwd(password, employer['password']):
            user = employer
        else:
            return {"error": f"Wrong password"}
    elif user_type == 'employee':
        employee = employee_collection.find_one({'email': email})
        if employee is None:
            return {"error": f"Invalid email"}
        if password == employee['id']:
            user = employee
        else:
            return {"error": f"Wrong password"}
    else:
        return {"error": f"[ {user_type} ] is not a valid user type."}

    del user['_id']
    return user


@app.delete("/user/{user_type}")
def delete_user_by_type(user_type, email: str, password: str):
    """Delete a employer or employee from DataBase"""
    user = None

    if user_type == 'employer':
        employer = employer_collection.find_one({'email': email})
        if employer is None:
            return {"error": f"Invalid email"}
        if check_pwd(password, employer['password']):
            employer_collection.delete_one({'email': email})
        else:
            return {"error": f"Wrong password"}
    elif user_type == 'employee':
        employee = employee_collection.find_one({'email': email})
        if employee is None:
            return {"error": f"Invalid email"}
        if password == employee['id']:
            employee_collection.delete_one({'email': email})
        else:
            return {"error": f"Wrong password"}
    else:
        return {"error": f"[ {user_type} ] is not a valid user type."}

    return {"message": f"The user_type [ {user_type} ] with the email \
[ {email} ] was deleted successfully"}


@app.post("/add_employer")
def add_employer(employer: Employer):
    """Insert Employer instance into the DataBase"""
    try:
        employer.hash_password()
        employer_collection.insert_one(dict(employer))
    except Exception:
        return {"error": f"Email [ {employer.email} ] is already in use."}
    return employer


@app.post("/add_employee")
def add_employee(employee: Employee):
    """Insert Employee instance into the DataBase"""
    employee_collection.insert_one(dict(employee))
    return employee


@app.get("/employer/get_employees")
def get_all_employees_for_employer(email: str, password: str):
    """Get all employees who's employer_id is
    equal to employer's id
    """
    id = None
    all_employees = []

    employer = employer_collection.find_one({'email': email})
    if employer is None:
        return {"error": f"Invalid email"}
    if check_pwd(password, employer['password']):
        id = employer['id']
    else:
        return {"error": f"Wrong password"}

    employees = employee_collection.find({'employer_id': str(id)})

    for employee in employees:
        del employee['_id']
        all_employees.append(employee)

    return all_employees


@app.put("/employer/change_password")
def get_all_employees_for_employer(email: str, password: str, new_pwd: str):
    """Change Employer user's password"""

    employer = employer_collection.find_one({'email': email})
    if employer is None:
        return {"error": f"Invalid email"}
    if check_pwd(password, employer['password']):
        if hash_pwd(new_pwd) == employer['password']:
            return {"error": f"Password already in use"}
        else:
            employer = employer_collection.update_one(
                {'email': email}, {"$set": {'password': hash_pwd(new_pwd)}})
    else:
        return {"error": f"Wrong password!"}

    return {'message': "Password changed successfully."}


@app.get("/calendar")
def all_calendar():
    """Get all calendars from the DataBase"""
    list_of_calendars = []
    calendars = calendar_collection.find()

    for calendar in calendars:
        del calendar['_id']
        list_of_calendars.append(calendar)

    return list_of_calendars


@app.get("/calendar/{user_type}")
def all_employers_calendar(user_type, email: str, password: str):
    """Get all calendars where employer id is present"""
    list_of_calendars = []
    calendars = []

    if user_type == 'employer':
        employer = employer_collection.find_one({'email': email})
        if employer is None:
            return {"error": f"Invalid email"}
        if check_pwd(password, employer['password']):
            calendars = calendar_collection.find(
                {'employer_id': employer['id']})
        else:
            return {"error": f"Wrong password"}
    elif user_type == 'employee':
        employee = employee_collection.find_one({'email': email})
        if employee is None:
            return {"error": f"Invalid email"}
        if password == employee['id']:
            calendars = calendar_collection.find(
                {'employee_id': employee['id']})
        else:
            return {"error": f"Wrong password"}
    else:
        return {"error": f"[ {user_type} ] is not a valid user type."}

    for calendar in calendars:
        del calendar['_id']
        list_of_calendars.append(calendar)

    return list_of_calendars


@app.put("/calendar/current_week")
def current_calendar_week(email: str, password: str, curr_calendar: Calendar):
    """Create or Update current week's calendar"""
    calendar = None

    employee = employee_collection.find_one({'email': email})
    if employee is None:
        return {"error": f"Invalid email"}
    if password == employee['id']:
        dt_calendar = time_date()
        w_id = f"{dt_calendar[1]}|{employee['id']}|{employee['employer_id']}"
        calendar = calendar_collection.find_one({"week_id": w_id})
        if calendar is None:
            curr_calendar.employee_id = employee['id']
            curr_calendar.employer_id = employee['employer_id']
            curr_calendar.week_id = w_id
            curr_calendar.week_start_end = {
                'Sunday': dt_calendar[1],
                'Saturday': dt_calendar[2]
            }
            calendar_collection.insert_one(dict(curr_calendar))
        else:
            calendar_collection.update(
                {'week_id': curr_calendar.week_id}, {'$set': {
                    'sunday':  curr_calendar.sunday,
                    'monday':  curr_calendar.monday,
                    'tuesday':  curr_calendar.tuesday,
                    'wednesday':  curr_calendar.wednesday,
                    'thursday':  curr_calendar.thursday,
                    'friday':  curr_calendar.friday,
                    'saturday':  curr_calendar.saturday,
                }})
    else:
        return {"error": f"Wrong password"}

    calendar = calendar_collection.find_one({"week_id": w_id})
    del calendar['_id']

    return dict(calendar)
