from student_management.models import Admin, Instructor, Course, Student, StudentCourse
from werkzeug.security import generate_password_hash
from student_management import db
from student_management.utils import (random_char)
import datetime


def populate_db():
    admins = [
        {
            'first_name': 'Admin',
            'last_name': 'AdminOne',
            'email': 'admin1@gmail.com',
            'rc_number': '938737123',
            'school_mail': 'name@school.com',
            'is_superadmin': True,
            'password': 'password123',
        }
    ]
    instructors = [
        {'first_name': 'Instructor', 'last_name': 'InstructorOne',
            'email': 'Instructor1@gmail.com', 'password': 'password123', },
        {'first_name': 'Instructor', 'last_name': 'InstructorTwo',
            'email': 'Instructor2@gmail.com', 'password': 'password456', },
        {'first_name': 'Instructor', 'last_name': 'InstructorThree',
            'email': 'Instructor3@gmail.com', 'password': 'password789', },

    ]
    students = [
        {'first_name': 'Student', 'last_name': 'StudentOne',
            'email': 'student1@gmail.com', 'password': 'password123', },
        {'first_name': 'Student', 'last_name': 'StudentTwo',
            'email': 'student2@gmail.com', 'password': 'password123', },
    ]
    courses = [
        {'course_code': 'CEG123', 'credit_hours': 2, 'name': 'Computer Engineering'},
        {'course_code': 'GEG333', 'credit_hours': 3, 'name': 'General Engineering'},
        {'course_code': 'SEG217', 'credit_hours': 6, 'name': 'General Engineering'},
    ]
    for user in admins:
        identifier = random_char(10)
        current_year = str(datetime.datetime.now().year)
        admin = Admin(email=user['email'], first_name=user['first_name'], last_name=user['last_name'],
                      password_hash=generate_password_hash(user['password']), user_type='admin',
                      designation='Chief Administrator', identifier=identifier, rc_number=user['rc_number'],
                      school_mail=user['school_mail'], is_superadmin=user['is_superadmin']
                      )
        try:
            admin.save()
        except:
            db.session.rollback()

    for user in instructors:
        identifier = random_char(10)
        current_year = str(datetime.datetime.now().year)
        employee_no = 'INST@' + random_char(6) + current_year
        instructor = Instructor(email=user['email'], first_name=user['first_name'], last_name=user['last_name'],
                                password_hash=generate_password_hash(user['password']), user_type='Instructor',
                                employee_no=employee_no, identifier=identifier
                                )
        try:
            instructor.save()
        except:
            db.session.rollback()

    for course in courses:
        instructor = Instructor.query.filter_by(
            email='Instructor1@gmail.com').first()
        data = Course(course_code=course['course_code'], credit_hours=course['credit_hours'],
                      name=course['name'], instructor_id=instructor.id
                      )
        try:
            data.save()
        except:
            db.session.rollback()

    for user in students:
        identifier = random_char(10)
        current_year = str(datetime.datetime.now().year)
        admission_no = 'STD@' + random_char(6) + current_year
        student = Student(email=user['email'], first_name=user['first_name'], last_name=user['last_name'],
                          password_hash=generate_password_hash(user['password']), user_type='student',
                          admission_no=admission_no, identifier=identifier
                          )
        try:
            student.save()
            course = Course.query.filter_by(course_code='MAT564').first()
            student_course = StudentCourse(
                student_id=student.id, course_id=course.id)
            student_course.save()
        except:
            db.session.rollback()
