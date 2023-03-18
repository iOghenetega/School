from student_management.models import Course, Instructor
from student_management.student.serializers import students_fields_serializer
from student_management.utils import random_char
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from flask import request
from ..serializer_course import course_retrieve_fields_serializer


courses_namespace = Namespace('courses', description='Namespace for courses')


course_creation_serializer = courses_namespace.model(
    'Course creation serializer', {
        'name': fields.String(required=True, description="A course name"),
        # 'course_code': fields.String(description="A course code"),
        'instructor_id': fields.Integer(required=True, description="Course instructor id"),
    }
)


student_course_register_serializer = courses_namespace.model(
    'Student Course Creation Serializer', {
        'student_id': fields.String(required=True, description="A student id"),
    }
)

students_serializer = courses_namespace.model(
    'Student Serializer', students_fields_serializer)

register_fields_serializer = {
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Lat name"),
    'user_type': fields.String(required=True, description="User type(Role)"),
    'password': fields.String(required=True, description="A password"),
}

course_instructor_serializer = courses_namespace.model(
    'Course instructor serializer', {
        'identifier': fields.String(description='User email address'),
        'email': fields.String(required=True, description='User email address'),
        'first_name': fields.String(required=True, description="First name"),
        'last_name': fields.String(required=True, description="Lat name"),
        'employee_no': fields.String(required=True, description="Course instructor id"),
        'created_at': fields.DateTime(description="Course creation date"),
    }
)
course_retrieve_serializer = courses_namespace.model(
    'Course Retrieval serializer', course_retrieve_fields_serializer)


@courses_namespace.route('')
class StudentsScoreAddView(Resource):

    @courses_namespace.marshal_with(course_retrieve_serializer)
    def get(self):
        courses = Course.query.all()
        return courses, HTTPStatus.OK

    @courses_namespace.expect(course_creation_serializer)
    def post(self):
        data = request.get_json()
        instructor = Instructor.query.filter_by(
            id=data.get('instructor_id')).first()
        if instructor:
            code = random_char(10)
            course = Course(
                course_code=code,
                instructor_id=instructor.id,
                name=data.get('name'),
            )
            try:
                course.save()
                return {'message': 'Course registered successfully'}, HTTPStatus.CREATED
            except:
                return {'message': 'An error occurred while saving course'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'Invalid Instructor id'}, HTTPStatus.BAD_REQUEST
