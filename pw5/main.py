import tarfile
import os
import glob

from input import *
from output import *
from domains.container import *

def compress_data():
    with tarfile.open('students.dat', 'w:gz') as tf:
        for filename in ['students.txt', 'courses.txt', 'marks.txt']:
            if os.path.isfile(filename):
                tf.add(filename)

def decompress_data():
    with tarfile.open('students.dat', 'r:gz') as tf:
        tf.extractall()

def import_students_info(data):
    for line in data:
        s = Student()
        s.import_info()
        Container.students.append(s)

def import_courses_info(data):
    for line in data:
        c = Course()
        c.import_info()
        Container.courses.append(c)

def import_marks_info(data):
    for line in data:
        course_name, student_name, value = line.split(' --- ')
        course = next(filter(lambda c: c.get_name() == course_name, Container.courses))
        student = next(filter(lambda s: s.get_name() == student_name, Container.students))
        course.add_mark(float(value), student)
        student.add_mark(float(value), course)

def exit_program():
    compress_data()
    for filename in glob.glob('*.txt'):
        os.remove(filename)
    return -10

def main():
    curses.wrapper(curse_splash_screen)
    cmdp = CommandPrompt('Enter a command:', CommandList([
                ('Input student info', input_student_info),
                ('Input course info', input_course_info),
                ('Input marks of a course', input_marks),
                ('Show students', list_students),
                ('Show courses', list_courses),
                ('Show marks of a course', list_marks),
                ('Calculate GPA of a student', calculate_gpa),
                ('Exit', exit_program)]), '[1-8]')
    cmdp.main_loop()

if __name__ == '__main__':
    if os.path.isfile('students.dat'):
        decompress_data()
        for filename in glob.glob('*.txt'):
            with open(filename, 'r') as f:
                data = f.read().splitlines()
                if filename == 'students.txt':
                    import_students_info(data)
                elif filename == 'courses.txt':
                    import_courses_info(data)
        with open('marks.txt', 'r') as f:
            data = f.read().splitlines()
            import_marks_info(data)
    main()
