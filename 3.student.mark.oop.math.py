import re
import sys
import math
import numpy

class Student:
    def __init__(self, student_id, student_dob, student_name):
        self.__id = student_id
        self.__dob = student_dob
        self.__name = student_name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    @staticmethod
    def get_info_header():
        return f'{"ID":^15}{"DATE OF BIRTH":^20}{"NAME":^20}'

    def get_info(self):
        return f'{self.__id:^15}{self.__dob:^20}{self.__name:>20}'

class Course:
    def __init__(self, course_id, course_name):
        self.__id = course_id
        self.__name = course_name
        self.__marksheet = Marksheet()

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    @staticmethod
    def get_info_header():
        return f'{"ID":^15}{"NAME":^50}'

    def get_info(self):
        return f'{self.__id:>15}{self.__name:>50}'

    def add_mark(self, student, mark):
        self.__marksheet.update(student, mark)

    def show_marks(self):
        print(Marksheet.get_info_header())
        for (student, mark) in self.__marksheet.get_list():
            print(f'{student.get_name():>20}{mark:^10}')

class Marksheet:
    def __init__(self):
        self.__marksheet = []

    @staticmethod
    def get_info_header():
        return f'{"STUDENT NAME":^20}{"MARK":^10}'

    def has_marks(self):
        return bool(self.__marksheet)

    def update(self, student, mark):
        self.__marksheet.append((student, mark))

    def get_mark_of(self, student):
        res = list(filter(lambda x: x[0].get_id() == student.get_id(), self.__marksheet))
        if res:
            return res[0][1]
        return False

    def get_list(self):
        return self.__marksheet

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
        try:
            return self.__cmd_list.get_command(cmd_num-1)['callback']()
        except:
            print(f'Error: {sys.exc_info()}')

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
    user_input_name = Validator(input('Enter course name: '), '[A-Za-z][A-Za-z ]*')
    if user_input_id.is_ok() and user_input_name.is_ok():
        return tuple(map(Validator.value, [user_input_id, user_input_name]))
    return (None, None)

def input_mark_details(course):
    def input_mark_details_specific():
        print(f'Input marks for course [{course.get_name()}]:')
        for student in Container.students:
            user_input_mark = Validator(
                input(f'Enter mark of student [{student.get_name()}]: '),
                '[0-9.]+')
            if user_input_mark.is_ok():
                course.add_mark(student, math.floor(user_input_mark.value(float)))
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
        course_id, course_name = input_course_details()
        if not (course_id and course_name):
            return False
        Container.courses.append(Course(course_id, course_name))
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

if __name__ == '__main__':
    cmdp = CommandPrompt('Enter a command:', CommandList([
                ('Input student info', input_student_info),
                ('Input course info', input_course_info),
                ('Input marks of a course', input_marks),
                ('Show students', list_students),
                ('Show courses', list_courses),
                ('Show marks of a course', list_marks),
                ('Exit', lambda: -10)]), '[1-7]')
    cmdp.main_loop()
