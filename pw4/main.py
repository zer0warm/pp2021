from input import *
from output import *

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
