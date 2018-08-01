# -*- encoding: utf-8 -*-
from psycopg2 import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger  # noqa


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
    # Mute SQL error
    @mute_logger('odoo.sql_db')
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

    # Mute SQL error
    @mute_logger('odoo.sql_db')
    def test_02_two_course_same_name(self):
        """
        Test two create two course with same name.
        To raise constraint of unique name.
        """
        test_02_two_course_same_name_correct = False
        try:
            new_id = self.create_course('test1', 'test_description', None)
            print(bcolors.OKBLUE, "new id: ", new_id, bcolors.ENDC)
            new_id2 = self.create_course('test1', 'test_description', None)
            print(bcolors.OKBLUE, "new id2: ", new_id2, bcolors.ENDC)
        except IntegrityError:
            test_02_two_course_same_name_correct = True

        self.assertTrue(test_02_two_course_same_name_correct)

    # Mute SQL error
    @mute_logger('odoo.sql_db')
    def test_03_duplicate_course(self):
        """
        Test to duplicate a course and check that work fine!
        """
        course = self.env.ref('openacademy.course0')
        course_id = course.copy()
        print(bcolors.OKBLUE, "copy course id: ", course_id, bcolors.ENDC)
