# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


def get_uid(self, *a):
    return self.env.uid


class Course(models.Model):
    _name = "openacademy.course"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
        "res.users",
        string="Responsible",
        index=True,
        ondelete="set null",
        default=get_uid
    )
    sessions_id = fields.One2many("openacademy.session", "course_id")

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [("name", "=like", u"Copy of {}".format(self.name))]
        )
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default["name"] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ("name_description_check",
         "CHECK(name != description)",
         "The title of the course should not be the description"),

        ("name_unique",
         "UNIQUE(name)",
         "The course title must be unique"),
    ]


class Session(models.Model):
    _name = "openacademy.session"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    datetime_test = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one(
        "res.partner",
        string="Instructor",
        domain=[
            '|',
            ('instructor', '=', True),
            ('category_id', 'ilike', "Teacher")
        ]
    )
    course_id = fields.Many2one(
        "openacademy.course",
        string="Course",
        ondelete="cascade",
        required=True
    )
    attendee_ids = fields.Many2many("res.partner", string="Attendees")
    taken_seats = fields.Float(compute="_taken_seats")
    active = fields.Boolean(default=True)

    @api.depends("seats", "attendee_ids")
    def _taken_seats(self):
        for record in self.filtered(lambda r: r.seats):
            record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats

    @api.onchange("seats", "attendee_ids")
    def _verify_valid_seats(self):
        if self.filtered(lambda r: r.seats < 0):
            self.active = False
            return {
                "warning": {
                    "title": "Incorrect 'seats' value",
                    "message": "The number of available seats may not be negative"
                }
            }
        if self.seats < len(self.attendee_ids):
            self.active = False
            return {
                "warning": {
                    "title": "Too many attendees",
                    "message": "Increase seats or remove excess attendees"
                }
            }
        self.active = True

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError(
                    "A session's instructor can't be an attendee"
                )
