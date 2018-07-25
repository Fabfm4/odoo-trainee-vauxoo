# -*- encoding: utf-8 -*-
from psycopg2 import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class GlobalTestOpenAcademyCourse(TransactionCase):
    """
    Global test to openacademy course model.
    Test create course and trigger contraints.
    """
    # Method seudo-constructor of test setUp
    def setUp(self):
        # Define global variables to test methods
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.variable = "hello world"
        self.course = self.env['openacademy.course']

    # Method of class that is not test
    def create_course(self, name, description, responsable_id):
        course_id = self.course.create({
            'name': name,
            'description': description,
            'responsable_id': responsable_id
        })
        return course_id

    # Method of test starts with 'def test_*(self):'1
    def test_01_same_name_description(self):
        """
        Test create a course with same name and description.
        To test contraint of name different to description.
        """
        test_01_same_name_description_correct = False
        try:
            self.create_course('test', 'test', None)
        except IntegrityError:
            test_01_same_name_description_correct = True

        self.assertTrue(test_01_same_name_description_correct)
