# -*- encoding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger  # noqa
from odoo.exceptions import ValidationError


class GlobalTestOpenAcademySession(TransactionCase):
    """
    This create global test to sessions
    """

    # Seudo constructor method
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env["openacademy.session"]

    # Generic Methods
    def create_session(self, name, seats, instructor, course, attendees=None):
        data = {
            'name': name,
            'seats': seats,
            'instructor_id': instructor.id,
            'course_id': course.id,
        }
        if attendees is not None:
            data['attendee_ids'] = [(6, 0, attendees)]

        return self.session.create(data)

    # Test methods
    def test_04_instructor_is_attendee(self):
        """
        Check that raise of 'A session's instructor can't be an attendee
        """
        test_04_instructor_is_attendee_correct = False
        try:
            partner_vauxoo = self.env.ref('base.res_partner_2')
            course = self.env.ref('openacademy.course0')
            self.create_session(
                name='Session test 1',
                seats=1,
                instructor=partner_vauxoo,
                course=course,
                attendees=[partner_vauxoo.id]
            )
        except ValidationError as vaidation_error:
            test_04_instructor_is_attendee_correct = True
            self.assertEquals(
                vaidation_error.name, (
                    "A session's instructor can't be an attendee"
                )
            )

        self.assertTrue(test_04_instructor_is_attendee_correct)

    def test_05_create_valid_session(self):
        """
        Check that raise of 'A session's instructor can't be an attendee
        """
        partner_vauxoo = self.env.ref('base.res_partner_1')
        partner_attendee = self.env.ref('base.res_partner_2')
        course = self.env.ref('openacademy.course0')
        session = self.create_session(
            name='Session test 1',
            seats=1,
            instructor=partner_vauxoo,
            course=course,
            attendees=[partner_attendee.id]
        )
        self.assertIsNotNone(session)
