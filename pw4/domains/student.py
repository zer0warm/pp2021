import math
import numpy as np
from domains.course import *
from domains.mark import *

class Student(MarkManager):
    def __init__(self, student_id, student_dob, student_name):
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
