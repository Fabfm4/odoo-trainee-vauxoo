# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _


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
         _("The title of the course should not be the description")),

        ("name_unique",
         "UNIQUE(name)",
         _("The course title must be unique")),
    ]


class Session(models.Model):
    _name = "openacademy.session"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    datetime_test = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    color = fields.Float()

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
    end_date = fields.Date(
        string="End Date",
        store=True,
        compute="_get_end_date",
        inverse='_set_end_date',
    )

    attendees_count = fields.Integer(
        string="Attendees count",
        compute="_get_attendees_count",
        store=True
    )

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    @api.depends("seats", "attendee_ids")
    def _taken_seats(self):
        for record in self.filtered(lambda r: r.seats):
            seats = record.seats
            record.taken_seats = 100.0 * len(record.attendee_ids) / seats

    @api.onchange("seats", "attendee_ids")
    def _verify_valid_seats(self):
        if self.filtered(lambda r: r.seats < 0):
            self.active = False
            return {
                "warning": {
                    "title": _("Incorrect 'seats' value"),
                    "message": _(
                        "The number of available seats may not be negative"
                    )
                }
            }
        if self.seats < len(self.attendee_ids):
            self.active = False
            return {
                "warning": {
                    "title": _("Too many attendees"),
                    "message": _("Increase seats or remove excess attendees")
                }
            }
        self.active = True

    @api.depends("start_date", "duration")
    def _get_end_date(self):
        for record in self.filtered('start_date'):
            start = fields.Datetime.from_string(record.start_date)
            duration = timedelta(days=record.duration, seconds=-1)
            record.end_date = start + duration

    def _set_end_date(self):
        for record in self:
            if not (record.start_date and record.end_date):
                continue

            start_date = fields.Datetime.from_string(record.start_date)
            end_date = fields.Datetime.from_string(record.end_date)
            record.duration = (end_date - start_date).days + 1

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id and record.instructor_id in record.attendee_ids:  # noqa
                raise exceptions.ValidationError(
                    _("A session's instructor can't be an attendee")
                )
