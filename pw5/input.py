from domains.student import *
from domains.course import *
from domains.mark import *
from domains.validator import *
from domains.command import *
from domains.container import *

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
                course.get_mark(student).export_info()
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
        new_student = Student(student_id, student_dob, student_name)
        new_student.export_info()
        Container.students.append(new_student)
    return True

def input_course_info():
    n = input_number_of_courses()
    if n == -1:
        return False
    for _ in range(n):
        course_id, course_name, course_ects = input_course_details()
        if not (course_id and course_name and course_ects):
            return False
        new_course = Course(course_id, course_name, course_ects)
        new_course.export_info()
        Container.courses.append(new_course)
    return True

def input_marks():
    cmds = CommandList()
    for course in Container.courses:
        mark_note = ' (graded)' if course.has_marks() else ' (not graded)'
        cmds.add(course.get_name() + mark_note, input_mark_details(course))
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
