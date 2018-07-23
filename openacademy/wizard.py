# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = "openacademy.wizard"

    def _default_session(self):
        session_obj = self.env["openacademy.session"]
        session_ids = self._context.get("active_ids")
        session_records = session_obj.browse(session_ids)
        return session_records

    session_id = fields.Many2many(
        'openacademy.session',
        string="Session",
        requiered=True,
        default=_default_session
    )
    attendee_ids = fields.Many2many('res.partner', string="Ateendees")

    @api.multi
    def subscribe(self):
        for session in self.session_id:
            session.attendee_ids |= self.attendee_ids
        return {}
