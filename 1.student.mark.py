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

def show_student_marks_of_course(course):
    print(f"Show marks of the course {course['name']}:")

    for student, mark in course['marks']:
        print(f"-> {student['name']}: {mark}")

if __name__ == '__main__':
    students = []
    courses = []
    
    for _ in range(get_number_of_students()):
        students.append(get_student_information())

    for _ in range(get_number_of_courses()):
        courses.append(get_course_information())

    for course in courses:
        update_marks_of_course(course)

    list_courses()
    list_students()

    for course in courses:
        show_student_marks_of_course(course)
