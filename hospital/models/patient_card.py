# -*- coding: utf-8 -*-
"""hospital management table"""

from odoo import api, fields, models, _


class PatientCard(models.Model):
    """For Patient Card"""
    _name = "patient.card"
    _inherit = "mail.thread"
    _description = "Patient Card"
    _rec_name = "patient"


    patient = fields.Char(string='Patient ID',
                             readonly=True, default=lambda self: _('New'))
    name = fields.Char(string='Patient Name')
    patient_name = fields.Char(string='Patient Name')
    partner_id = fields.Many2one("res.partner",
                                 string='Patient Name', required=True)
    dob = fields.Date(related="partner_id.dob", string='DOB')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')],
        string='Gender', related="partner_id.gender")
    partner_invoice_id = fields.Many2one("res.partner",
                                         string="Address")
    mobile = fields.Char(related="partner_id.mobile", string='Mobile')
    phone = fields.Char(related="partner_id.phone", string='Phone')
    blood_group = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')],
        string='Blood Group')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm')], string='Status', tracking=True,
        default='draft')

    history_ids = fields.One2many('patient.op',
                                  'patient_card_id',
                                  string="OP History", readonly=1)
    appointment_count = fields.Integer(compute='_compute_count')

    def _compute_count(self):
        """computes the count of appointments"""
        for record in self:
            record.appointment_count = self.env['dr.appointment'].search_count(
                [('partner_id', '=', self.partner_id.id)])

    # def _compute_name(self):
    #     """This function is to get the name along with sit sequence no:"""
    #     for record in self:
    #         if record.patient_id and record.partner_id:
    #             record.name = "[{0}] : {1}".format(
    #                 record.patient_id, record.partner_id.name)

    def name_get(self):
        """Override name_get to return name and sequence number"""
        result = []
        for record in self:
            result.append((record.id, '{} : {}'.format(record.patient,
                                                       record.partner_id.name)))
        return result

    def action_appointment_wizard(self):
        """function for redirect to another model"""
        return {
            'name': _('Appointment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.appointment',
            'type': 'ir.actions.act_window',
            'context': {'default_patient_card_id': self.id},
            'target': 'new',
        }

    def get_appointment(self):
        """function for get the smart button of appointment"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'view_mode': 'tree,form',
            'res_model': 'dr.appointment',
            'domain': [('partner_id', '=', self.partner_id.id)]
        }

    @api.model
    def create(self, vals):
        """ GENERATING SEQUENCE"""
        if vals.get('patient', _('New')) == _('New'):
            vals['patient'] = self.env['ir.sequence'].next_by_code(
                'patient.card') or _('New')
        return super().create(vals)

    @api.depends('dob')
    def _compute_age(self):
        """Calculates age based on dob"""
        today = fields.Date.today()
        for patient in self:
            if patient.dob:
                dob = fields.Date.from_string(patient.dob)
                patient.age = (today - dob).days // 365
            else:
                patient.age = 0
