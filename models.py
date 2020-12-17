"""Models"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict
from utils import hash_pwd, time_date
from uuid import uuid4


class Employer(BaseModel):
    """Employer class"""
    id = str(uuid4())
    first_name: str
    last_name: str
    email: str
    password: str
    date_created = datetime.now()

    def hash_password(self):
        """Hash Password"""
        self.password = hash_pwd(self.password)


class Employee(BaseModel):
    """Employee class"""
    id = str(uuid4())
    employer_id: str
    first_name: str
    last_name: str
    email: str
    date_created = datetime.now()


class WorkDescription(BaseModel):
    """WorkDescription class"""
    hour = 0
    location = ''
    description = ''


class Calendar(BaseModel):
    """Calendar class"""
    employer_id: str
    employee_id: str
    week_id: str
    week_start_end: Dict
    sunday = dict(WorkDescription())
    monday = dict(WorkDescription())
    tuesday = dict(WorkDescription())
    wednesday = dict(WorkDescription())
    thursday = dict(WorkDescription())
    friday = dict(WorkDescription())
    saturday = dict(WorkDescription())
    date_created = datetime.now()
