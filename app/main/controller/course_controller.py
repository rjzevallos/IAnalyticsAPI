from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CourseDto
from ..service.course_service import save_new_course, get_all_courses, get_a_course,delete_a_course,update_a_course

api = CourseDto.api
_course = CourseDto.course


@api.route('/')
class CourseList(Resource):
    @api.doc('list_of_registered_courses') 
    @api.marshal_list_with(_course, envelope='data')
    def get(self):
        """List all registered courses"""
        return get_all_courses()

    @api.expect(_course, validate=True)
    @api.response(201, 'Course successfully created.')
    @api.doc('create a new course')
    def post(self):
        """Creates a new Course """
        data = request.json
        return save_new_course(data=data)


@api.route('/<course_name>')
@api.param('course_name', 'The course identifier')
@api.response(404, 'Account not found.')
class Course(Resource):
    @api.doc('get an course')
    @api.marshal_with(_course)
    def get(self, course_name):
        """get an course given its identifier"""
        course = get_a_course(course_name)
        if not course:
            api.abort(404)
        else:
            return course

    @api.doc('delete a course')
    @api.marshal_with(_course)        
    def delete(self,course_name):
        """delete a course given its identifier"""
        delete_a_course(course_name)
        
    @api.doc('update a course')
    @api.marshal_with(_course)        
    def put(self,course_name):
        """update a course given its identifier"""
        course = update_a_course(course_name)
        if not course:
            api.abort(404)
        else:
            return course        


