import curses
from domains.student import *
from domains.course import *
from domains.mark import *
from domains.validator import *
from domains.command import *
from domains.container import *

def list_students():
    if len(Container.students) == 0:
        print('No students available.')
    else:
        print('List of students:')
        print(f'{"ID":^15}{"DATE OF BIRTH":^20}{"NAME":^20}{"GPA":^5}')
        for student in Container.students:
            info = f'{student.get_id():^15}'
            info += f'{student.get_dob():^20}'
            info += f'{student.get_name():>20}'
            info += f'{(student.get_gpa() if student.get_gpa() else "NaN"):>5}'
            print(info)
    print()

def list_courses():
    if len(Container.courses) == 0:
        print('No courses available.')
    else:
        print('List of courses:')
        print(f'{"ID":^15}{"NAME":^50}{"ECTS":^5}{"GRADED":^10}')
        for course in Container.courses:
            info = f'{course.get_id():>15}'
            info += f'{course.get_name():>50}'
            info += f'{course.get_credits():>5}'
            info += f'{course.has_marks():^10}'
            print(info)
    print()

def list_mark_details(course):
    def list_mark_details_specific():
        print(f"Course [{course.get_name()}]'s marksheet:")
        print(f'{"STUDENT NAME":^20}{"MARK":^10}')
        for mark in course.show_marks():
            student = mark.get_object(Student)
            print(f'{student.get_name():<20}{mark.get_value():^10}')
    return list_mark_details_specific

def list_marks():
    cmds = CommandList()
    for course in Container.courses:
        mark_note = ' (graded)' if course.has_marks() else ' (not graded)'
        cmds.add(course.get_name() + mark_note, list_mark_details(course))
    cmds.add('Return to menu', lambda: -10)
    cmdp = CommandPrompt('Choose a course:',
                         cmds,
                         f'[1-{cmds.get_length()}]')
    cmdp.main_loop()

def curse_splash_screen(stdscr):
    stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')
    s = "Curses is still in development..."
    stdscr.addstr(curses.LINES//2-1, curses.COLS//2-len(s)//2, s)
    s = "Press any key to continue in CLI mode"
    stdscr.addstr(curses.LINES//2+1, curses.COLS//2-len(s)//2, s)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.getkey()

if __name__ == '__main__':
    curses.wrapper(curse_splash_screen)
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
