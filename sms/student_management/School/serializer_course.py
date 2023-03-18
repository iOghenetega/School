from flask_restx import fields


course_retrieve_fields_serializer = {
    'id': fields.Integer(),
    'name': fields.String(required=True, description="The course name"),
    'course_code': fields.String(description="The course code"),
    'instructor_id': fields.Integer(),
    'created_at': fields.DateTime(description="Course creation date"),
}
