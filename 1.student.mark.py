def get_number_of_students():
    return int(input('Enter number of students: '))

def get_student_information():
    return {'id': input('---> Enter student id: '),
            'name': input('---> Enter student name: '),
            'dob': input("---> Enter student's date of birth: ")}

def get_number_of_courses():
    return int(input('Enter number of courses: '))

def get_course_information():
    return {'id': input('---> Enter course id: '),
            'name': input('---> Enter course name: ')}

def update_marks_of_course(course):
    print(f"-> Enter marks for the course {course['name']}:")
    course['marks'] = []

    for student in students:
        course['marks'].append((student,
            input(f"---> Enter mark for student {student['name']}: ")))

def list_courses():
    print('Listing available courses:')

    for course in courses:
        print(f"* [{course['id']}] {course['name']}")

def list_students():
    print('Listing students:')

    for student in students:
        print(f"* ({student['id']}) <{student['dob']}> {student['name']}")

def show_marks_of_course(course):
    print(f"Show marks of the course {course['name']}:")

    for student, mark in course['marks']:
        print(f"-> {student['name']}: {mark}")

def select_course_prompt(intro_message):
    list_courses()
    print(intro_message)

    return input('---> Choose a course (Enter nothing to skip): ')

def search(List, keyword):
    for item in List:
        if keyword in item.values():
            return item

    empty_item = List[0].copy()
    empty_item.clear()
    return empty_item

def action_loop(msg=None, callback=None):
    while True:
        keyword = select_course_prompt(f'-> {msg}')
        if not keyword:
            print()
            break
        callback(search(courses, keyword))
        print()

if __name__ == '__main__':
    students = []
    courses = []

    for _ in range(get_number_of_students()):
        students.append(get_student_information())

    for _ in range(get_number_of_courses()):
        courses.append(get_course_information())

    list_students()
    action_loop(msg='Marking courses...', callback=update_marks_of_course)
    action_loop(msg='Select a course to show marks...', callback=show_marks_of_course)

    print('Thank you for using the service!')
