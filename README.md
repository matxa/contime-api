# ConTime API
## ConTime API is the bridge between the backend and the frontend of the [ConTime Web Application](https://github.com/matxa/ConTime).
<hr>

&#10240;

### Technologies & Tools used :
- [Python](https://www.python.org/) v3.8.5
    - [FastAPI](https://fastapi.tiangolo.com/) - "A modern, fast, web framework for building APIs..."
    - [Pydantic](https://pydantic-docs.helpmanual.io/) - "Data validation and settings management using python type annotations."
    - [Typing](https://fastapi.tiangolo.com/python-types/#generic-types-with-type-parameters) - A standard Python module for declaring datatypes like [dict, list, set, tuple].
    - [PyMongo](https://pymongo.readthedocs.io/en/stable/tutorial.html) - "A Python distribution containing tools for working with MongoDB..."
- [MongoDB](https://www.mongodb.com/1) - "A document database, which means it stores data in JSON-like documents..."

&#10240;

### ConTime API Roles:

- CREATE new users and calendars.
    - There are two types of user [ employer, employee ]
    - A calendar can only be created by a employee ( user_type )
- UPDATE or DELETE existing users, and calendars.
    - Update employer's password.

&#10240;

## Schemas &#10240; &#123; &#34; &#34; &#58; &#34; &#34; &#125;

- __( user_type ) employer__
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "password": "string",
  "id": "unique_id",
  "date_created": "date_time"
}
```
- __( user_type ) employee__
```json
{
  "employer_id": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "id": "unique_id",
  "date_created": "date_time"
}
```
- __Calendar__
```json
{
  "employer_id": "string",
  "employee_id": "string",
  "week_id": "string",
  "week_start_end": {},
  "sunday": {
    "hour": 0,
    "location": "",
    "description": ""
  },
  "monday": {
    "hour": 0,
    "location": "",
    "description": ""
  },
  "tuesday": {
    "hour": 0,
    "location": "",
    "description": ""
  },
  "wednesday": {
    "hour": 0,
    "location": "",
    "description": ""
  },
  "thursday": {
    "hour": 0,
    "location": "",
    "description": ""
  },
  "friday": {
    "hour": 0,
    "location": "",
    "description": ""
  },
  "saturday": {
    "hour": 0,
    "location": "",
    "description": ""
  },
  "date_created": "date_time"
}
```
&#10240;
## Routes &#10240; &#8634; &#8635;
&#10240;
- <mark style="background-color: #7bb3ba">"&#10240;/&#10240;"</mark>&#10240; &#11138; &#10240; [ 'GET' ] &#10240; &#10236; &#10240; Home of ConTime API, This route redirects to '/docs' route, if using applications such as [PostMan](https://www.postman.com/) it is recommended to visit <mark style="background-color: #bfc28d;">' /openapi.json '</mark>  route instead.

- <mark style="background-color: #7bb3ba">" /users/{user_type} "</mark>&#10240; &#11138; &#10240; [ 'GET' ]&#10240; &#10236; &#10240; Get all employers or employees from DataBase.

- <mark style="background-color: #7bb3ba">" /user/{user_type} "</mark>&#10240; &#11138; &#10240; [ 'GET' , 'DELETE' ]&#10240; &#10236; &#10240; Get or delete a employer or employee from DataBase.
    - Authentication &#58; &#10240; Use user's __email__ and __password__

- <mark style="background-color: #7bb3ba">" /add_employer "</mark>&#10240; &#11138; &#10240; [ 'POST' ]&#10240; &#10236; &#10240; Insert a new Employer instance into the DataBase.

- <mark style="background-color: #7bb3ba">" /add_employee "</mark>&#10240; &#11138; &#10240; [ 'POST' ]&#10240; &#10236; &#10240; Insert a new Employee instance into the DataBase.

- <mark style="background-color: #7bb3ba">" /employer/get_employees "</mark>&#10240; &#11138; &#10240; [ 'GET' ]&#10240; &#10236; &#10240; Get all employees who's employer_id is equal to employer's id.
    - Authentication &#58; &#10240; Use user's __email__ and __password__

- <mark style="background-color: #7bb3ba">" /employer/change_password "</mark>&#10240; &#11138; &#10240; [ 'PUT' ]&#10240; &#10236; &#10240; Change Employer ( user_type ) password.
    - Authentication &#58; &#10240; Use user's __email__ and __password__

- <mark style="background-color: #7bb3ba">" /calendar "</mark>&#10240; &#11138; &#10240; [ 'GET' ]&#10240; &#10236; &#10240; Get all calendars from the DataBase.

- <mark style="background-color: #7bb3ba">" /calendar/{user_type} "</mark>&#10240; &#11138; &#10240; [ 'GET' ]&#10240; &#10236; &#10240; Get All of user's calendar.
    - Authentication &#58; &#10240; Use user's __email__ and __password__

- <mark style="background-color: #7bb3ba">" /calendar//calendar/current_week "</mark>&#10240; &#11138; &#10240; [ 'PUT' ]&#10240; &#10236; &#10240; Create or Update current week's calendar.
    - Authentication &#58; &#10240; Use user's __email__ and __password__

&#10240;<br>
<hr>
&#10240;<br>
Author: Marcelo Martins<br>
GitHub: @matxa<br>
Email: matxa21@gmail.com<br>
&#10240;
<hr>

