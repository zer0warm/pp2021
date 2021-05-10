from domains.mark import *
from domains.persistence import *

class Course(MarkManager):
    def __init__(self, course_id=None, course_name=None, course_credits=None):
        self.__id = course_id
        self.__name = course_name
        self.__ects = course_credits
        super().__init__()

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_credits(self):
        return self.__ects

    def show_marks(self):
        return self._marks

    def export_info(self):
        ds = DataStorage('courses.txt')
        ds.write(self)

    def import_info(self):
        ds = DataStorage('courses.txt')
        self.__id, self.__name, self.__ects = ds.read().split(' --- ')
        self.__ects = int(self.__ects)
