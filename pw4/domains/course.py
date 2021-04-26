from domains.mark import *

class Course(MarkManager):
    def __init__(self, course_id, course_name, course_credits):
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
