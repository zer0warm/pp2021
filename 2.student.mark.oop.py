class Student:
    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def dob(self):
        return self.__dob

    def set_info(self):
        self.__id = input('---> Enter student id: ')
        self.__name = input('---> Enter student name: ')
        self.__dob = input("---> Enter student's date of birth: ")
        
    def get_info(self):
        return f"{self.__id:<10}{self.__dob:<15}{self.__name:<20}"

class StudentList:
    def __init__(self):
        self.__list = []

    def get_content(self):
        return self.__list

    def details(self):
        print('Listing students:')
        print(f'{"ID":^10}{"DATE OF BIRTH":^15}{"NAME":^20}')
        for student in self.__list:
            print(student.get_info())
        print()

    def get_number_of_students(self):
        self.__len = int(input('-> Enter number of students: '))

    def bulk_add_students(self):
        self.get_number_of_students()
        for _ in range(self.__len):
            student = Student()
            student.set_info()
            self.__list.append(student)

class Course:
    def __init__(self):
        self.__marksheet = None

    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    
    def set_info(self):
        self.__id = input('---> Enter course id: ')
        self.__name = input('---> Enter course name: ')

    def get_info(self):
        return f"[{self.__id}] {self.__name}"

    def get_grade_status(self):
        course_info = f"[{self.__id}] {self.__name}"
        return f"{course_info}{' (graded)' if self.__marksheet else ''}"

    def show_marks(self):
        if self.__marksheet:
            self.__marksheet.show()
        else:
            print('This course has no marks.')

    def update_marks(self, students):
        self.__marksheet = Marksheet(self)
        print(f"-> Enter marks for the course {self.__name}:")
        for student in students.get_content():
            mark = input(f"---> Enter mark for student {student.name}: ")
            self.__marksheet.update(student, mark)

class CourseList:
    def __init__(self):
        self.__list = []

    def get_number_of_courses(self):
        self.__len = int(input('-> Enter number of courses: '))

    def search_course(self, query):
        for course in self.__list:
            if query in [course.name, course.ID]:
                return course
        return Course()

    def details(self, grade=False):
        print('Listing available courses:')
        for course in self.__list:
            print(course.get_grade_status() if grade else course.get_info())
        print()

    def bulk_add_courses(self):
        self.get_number_of_courses()
        for _ in range(self.__len):
            course = Course()
            course.set_info()
            self.__list.append(course)

    def bulk_update_marks(self, students):
        while True:
            print('-> Adding marks to database...')
            self.details(grade=True)
            query = input('---> Enter a course (Nothing to skip): ')
            if not query:
                print()
                break
            course = self.search_course(query)
            course.update_marks(students)
            print()

    def bulk_show_marks(self):
        while True:
            print('-> Showing marks of a course...')
            self.details(grade=True)
            query = input('---> Enter a course (Nothing to skip): ')
            if not query:
                print()
                break
            course = self.search_course(query)
            course.show_marks()
            print()

class Marksheet:
    def __init__(self, course):
        self.__course = course
        self.__sheet = []

    def update(self, student, mark):
        self.__sheet.append((student.ID, student.name, mark))

    def show(self):
        if self.__sheet:
            print(f'Show marks of course {self.__course.name}:')
            print(f'{"ID":^10}{"NAME":^20}{"MARK":^5}')
            for student_id, student_name, mark in self.__sheet:
                print(f'{student_id:<10}{student_name:<20}{mark:<5}')
        else:
            print('This course has no marks.')

if __name__ == '__main__':
    student_list = StudentList()
    course_list = CourseList()

    student_list.bulk_add_students()
    course_list.bulk_add_courses()

    student_list.details()
    course_list.details()
    
    course_list.bulk_update_marks(student_list)
    course_list.bulk_show_marks()

    print('Thank you for using the service!')
