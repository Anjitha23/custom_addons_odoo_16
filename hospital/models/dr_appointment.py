# -*- coding: utf-8 -*-

"""Appointment table"""

from odoo import fields, models, _


class DrAppointment(models.Model):
    """doctor appointment model"""
    _name = "dr.appointment"
    _description = "Doctors Appointment"
    _inherit = "mail.thread"
    _rec_name = "patient_card_id"

    patient_card_id = fields.Many2one('patient.card',
                                      string="Patient card", required=True)
    partner_id = fields.Many2one("res.partner", related='patient_card_id.partner_id',
                                 string='Patient Name')

    def add_doctor(self):
        """Add data to the existing module-job position:Doctor"""
        return [('job_id', '=', self.env.ref('hospital.doctor_job_position').id)]

    doctor_id = fields.Many2one('hr.employee', string='Doctor',
                                domain=add_doctor, required="True")
    user_id = fields.Many2one('res.users',related='doctor_id.user_id',string='User')
    department_id = fields.Many2one(related="doctor_id.department_id", string="Department")
    date = fields.Date(string='Date', default=lambda self: fields.Date.today())
    token = fields.Integer(string="Token No", readonly=1)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('appointment', 'Appointment'),
        ('op', 'Op'),
        ('cancel', 'Cancelled'),
    ], string='Status', tracking=True, default='draft')
    ticket_count = fields.Integer(compute='compute_count')
    op_ticket_id = fields.Many2one('patient.op', string=" ")
    phone = fields.Integer(string="Phone")

    def action_appointment(self):
        """function for appointment button"""
        if self.doctor_id and self.date:
            self.token = self._compute_next_token(self.doctor_id, self.date)
        self.write({'state': "appointment"})

    def action_op_wizard(self):
        """function for redirect to another model"""
        self.ensure_one()
        op_id = self.env['patient.op'].create({
            'patient_card_id': self.patient_card_id.id,
            'name_id': self.partner_id.id,
            'doctor_id': self.doctor_id.id,
            'date': self.date,
            'token': self.token,
            'appointment_id': self.id
        })
        self.op_ticket_id = op_id.id

        self.write({'state': "op"})
        return {
            'name': _('Patient Op'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'patient.op',
            'res_id': op_id.id,
            'type': 'ir.actions.act_window',
        }

    def get_op_ticket(self):
        """function for get the smart button of op tickets"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'OP Tickets',
            'view_mode': 'form',
            'res_model': 'patient.op',
            'res_id': self.op_ticket_id.id,
        }

    def compute_count(self):
        """computes the count of op tickets"""
        self.ticket_count = self.env['patient.op'].search_count(
            [('appointment_id', '=', self.id)])

    def _compute_next_token(self, doctor_id, date):
        """Token should be same order of OP tickets"""
        domain = [
            ('doctor_id', '=', doctor_id.id),
            ('date', '=', date)
        ]
        token_count = self.search_count(domain)
        return token_count
