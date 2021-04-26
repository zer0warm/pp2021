import re
import sys
import math
import numpy as np

class MarkManager:
    class Mark:
        def __init__(self, value, r_obj=None, e_obj=None):
            self.__value = value
            self.__manager = r_obj
            self.__managee = e_obj

        def get_value(self):
            return self.__value

        def get_object(self, _type):
            if isinstance(self.__manager, _type):
                return self.__manager
            return self.__managee

    def __init__(self):
        self._marks = []

    def add_mark(self, value, obj=None):
        mark = MarkManager.Mark(value, e_obj=obj)
        self._marks.append(mark)

    def get_mark(self, obj=None):
        for mark in self._marks:
            if mark.get_object(obj.__class__) == obj:
                return mark
        return False

    def has_marks(self):
        return bool(self._marks)

    @staticmethod
    def get_info_header():
        return f'{"STUDENT NAME":^20}{"MARK":^10}'

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

    @staticmethod
    def get_info_header():
        return f'{"ID":^15}{"DATE OF BIRTH":^20}{"NAME":^20}{"GPA":^5}'

    def get_info(self):
        info = f'{self.__id:^15}{self.__dob:^20}{self.__name:>20}'
        info += f'{(self.__gpa if self.__gpa else "NaN"):>5}'
        return info

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

    @staticmethod
    def get_info_header():
        return f'{"ID":^15}{"NAME":^50}{"ECTS":^5}'

    def get_info(self):
        return f'{self.__id:>15}{self.__name:>50}{self.__ects:>5}'

    def show_marks(self):
        print(MarkManager.get_info_header())
        for mark in self._marks:
            student = mark.get_object(Student)
            print(f'{student.get_name():<20}{mark.get_value():^10}')

class Validator:
    def __init__(self, raw_user_input, accept_pattern=None):
        self.__input = raw_user_input
        self.__pat = re.compile(f'^{accept_pattern}$')

    def is_ok(self):
        return re.search(self.__pat, self.__input)

    def value(self, value_type=str):
        return value_type(self.__input)

class CommandList:
    def __init__(self, cmd_list=None):
        self.__cmd_list = []
        if cmd_list and isinstance(cmd_list, list):
            for cmd_desc, cmd_callback in cmd_list:
                self.add(cmd_desc, cmd_callback)

    def add(self, cmd_desc, cmd_callback):
        cmd_validator = Validator(cmd_desc, '[A-Za-z][A-Za-z\'" ]+')
        if cmd_validator.is_ok() and callable(cmd_callback):
            self.__cmd_list.append({'desc': cmd_desc, 'callback': cmd_callback})
        else:
            raise Exception("Can't add command to list.")

    def list_commands(self):
        for i in range(len(self.__cmd_list)):
            desc = self.__cmd_list[i]['desc']
            print(f'[{i+1}] {desc}')

    def get_command(self, cmd_num):
        return self.__cmd_list[cmd_num]

    def get_length(self):
        return len(self.__cmd_list)

class CommandPrompt:
    state = -1

    def __init__(self, msg, cmd_list=None, pat=None):
        self.__prompt_msg = msg
        self.__cmd_list = cmd_list
        self.__accept_command_pattern = pat
        self.__PS = ['>>>', '->', '--->']
        CommandPrompt.state += 1

    def _list_commands(self):
        self.__cmd_list.list_commands()

    def _execute(self, cmd_num):
        return self.__cmd_list.get_command(cmd_num-1)['callback']()

    def _get_prompt_string(self):
        return self.__PS[CommandPrompt.state]

    def main_loop(self):
        while True:
            self._list_commands()
            cmd = Validator(
                    input(f'{self._get_prompt_string()} {self.__prompt_msg} '),
                    accept_pattern=self.__accept_command_pattern)
            if cmd.is_ok():
                status = self._execute(cmd.value(int))
                if status == -10:
                    CommandPrompt.state -= 1
                    break
                elif status == False:
                    print('Error: Invalid response. Try again.')
            else:
                print('Error: Invalid command. Try again.')

class Container:
    students = []
    courses = []

def input_number_of_courses():
    user_input = Validator(input('Enter number of courses: '), '[0-9]+')
    return user_input.value(int) if user_input.is_ok() else -1

def input_number_of_students():
    user_input = Validator(input('Enter number of students: '), '[0-9]+')
    return user_input.value(int) if user_input.is_ok() else -1

def input_student_details():
    user_input_id = Validator(input('Enter student ID: '), '.*')
    user_input_dob = Validator(input('Enter student date of birth: '), '[0-9]{2}/[0-9]{2}/[0-9]{4}')
    user_input_name = Validator(input('Enter student name: '), '[A-Za-z][A-Za-z ]*')
    if user_input_id.is_ok() and user_input_dob.is_ok() and user_input_name.is_ok():
        return tuple(map(Validator.value, [user_input_id, user_input_dob, user_input_name]))
    return (None, None, None)

def input_course_details():
    user_input_id = Validator(input('Enter course ID: '), '.*')
    user_input_name = Validator(input('Enter course name: '), '[A-Za-z][A-Za-z1-9. ]*')
    user_input_ects = Validator(input('Enter course credits: '), '[1-9]')
    if user_input_id.is_ok() and user_input_name.is_ok() and user_input_ects.is_ok():
        return (user_input_id.value(), user_input_name.value(), user_input_ects.value(int))
    return (None, None, None)

def input_mark_details(course):
    def input_mark_details_specific():
        print(f'Input marks for course [{course.get_name()}]:')
        for student in Container.students:
            user_input_mark = Validator(
                input(f'Enter mark of student [{student.get_name()}]: '),
                '[0-9.]+')
            if user_input_mark.is_ok():
                value = math.floor(user_input_mark.value(float))
                course.add_mark(value, student)
                student.add_mark(value, course)
            else:
                return False
    return input_mark_details_specific

def input_student_info():
    n = input_number_of_students()
    if n == -1:
        return False
    for _ in range(n):
        student_id, student_dob, student_name = input_student_details()
        if not (student_id and student_dob and student_name):
            return False
        Container.students.append(Student(student_id, student_dob, student_name))
    return True

def input_course_info():
    n = input_number_of_courses()
    if n == -1:
        return False
    for _ in range(n):
        course_id, course_name, course_ects = input_course_details()
        if not (course_id and course_name and course_ects):
            return False
        Container.courses.append(Course(course_id, course_name, course_ects))
    return True

def input_marks():
    cmds = CommandList()
    for course in Container.courses:
        cmds.add(course.get_name(), input_mark_details(course))
    cmds.add('Return to menu', lambda: -10)
    cmdp = CommandPrompt('Choose a course:',
                         cmds,
                         f'[1-{cmds.get_length()}]')
    cmdp.main_loop()

def list_students():
    if len(Container.students) == 0:
        print('No students available.')
    else:
        print('List of students:')
        print(Student.get_info_header())
        for student in Container.students:
            print(student.get_info())
    print()

def list_courses():
    if len(Container.courses) == 0:
        print('No courses available.')
    else:
        print('List of courses:')
        print(Course.get_info_header())
        for course in Container.courses:
            print(course.get_info())
    print()

def list_mark_details(course):
    def list_mark_details_specific():
        print(f"Course [{course.get_name()}]'s marksheet:")
        course.show_marks()
    return list_mark_details_specific

def list_marks():
    cmds = CommandList()
    for course in Container.courses:
        cmds.add(course.get_name(), list_mark_details(course))
    cmds.add('Return to menu', lambda: -10)
    cmdp = CommandPrompt('Choose a course:',
                         cmds,
                         f'[1-{cmds.get_length()}]')
    cmdp.main_loop()

def calculate_gpa_student(student):
    def calculate_gpa_student_specific():
        print(f'Calculate GPA for student [{student.get_name()}]...')
        student.calculate_gpa()
        print(f'Done, GPA = {student.get_gpa()}')
    return calculate_gpa_student_specific

def calculate_gpa():
    cmds = CommandList()
    for student in Container.students:
        cmds.add(f'{student.get_name()}', calculate_gpa_student(student))
    cmds.add('Return to menu', lambda: -10)
    cmdp = CommandPrompt('Choose a course:',
                         cmds,
                         f'[1-{cmds.get_length()}]')
    cmdp.main_loop()

if __name__ == '__main__':
    cmdp = CommandPrompt('Enter a command:', CommandList([
                ('Input student info', input_student_info),
                ('Input course info', input_course_info),
                ('Input marks of a course', input_marks),
                ('Show students', list_students),
                ('Show courses', list_courses),
                ('Show marks of a course', list_marks),
                ('Calculate GPA of a student', calculate_gpa),
                ('Exit', lambda: -10)]), '[1-8]')
    cmdp.main_loop()
