import tarfile
import os
import glob

from input import *
from output import *
from domains.container import *
from domains.mark import MarkManager

def compress_data():
    with tarfile.open('students.dat', 'w:gz') as tf:
        for filename in ['students.txt', 'courses.txt', 'marks.txt']:
            if os.path.isfile(filename):
                tf.add(filename)

def decompress_data():
    with tarfile.open('students.dat', 'r:gz') as tf:
        tf.extractall()

def import_students_info(data):
    for obj in data:
        Container.students.append(obj)

def import_courses_info(data):
    for obj in data:
        Container.courses.append(obj)

def import_marks_info(data):
    for obj in data:
        course = obj.get_object(Course)
        student = obj.get_object(Student)

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

def unpickle_data(f):
    u = pickle.Unpickler(f)
    data = []
    try:
        while True:
            data.append(u.load())
    except EOFError:
        pass
    return data

if __name__ == '__main__':
    if os.path.isfile('students.dat'):
        decompress_data()
        for filename in glob.glob('*.txt'):
            with open(filename, 'rb') as f:
                data = unpickle_data(f)
                if filename == 'students.txt':
                    import_students_info(data)
                elif filename == 'courses.txt':
                    import_courses_info(data)
        if os.path.isfile('marks.txt'):
            with open('marks.txt', 'rb') as f:
                data = unpickle_data(f)
                import_marks_info(data)
    main()
