import math
import numpy as np
from domains.course import *
from domains.mark import *
from domains.persistence import *

class Student(MarkManager):
    def __init__(self, student_id=None, student_dob=None, student_name=None):
        self.__id = student_id
        self.__dob = student_dob
        self.__name = student_name
        self.__gpa = None
        super().__init__()

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_gpa(self):
        return self.__gpa

    def __pre_calculate_gpa(self):
        self.__credits = []
        self.__mark_values = []
        for mark in self._marks:
            self.__credits.append(mark.get_object(Course).get_credits())
            self.__mark_values.append(mark.get_value())

    def calculate_gpa(self):
        self.__pre_calculate_gpa()
        self.__gpa = math.floor(np.average(
                np.array(self.__mark_values), weights=np.array(self.__credits)))

    def export_info(self):
        ds = DataStorage('students.txt')
        ds.write(f'{self.__id} --- {self.__dob} --- {self.__name}')

    def import_info(self):
        ds = DataStorage('students.txt')
        self.__id, self.__dob, self.__name = ds.read().split(' --- ')
