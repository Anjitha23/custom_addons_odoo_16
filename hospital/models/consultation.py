# -*- coding: utf-8 -*-
"""consultation table"""
from odoo import fields, models


class Consultation(models.Model):
    """consultation model"""
    _name = "consultation"
    _description = "Consultation Details"
    _inherit = "mail.thread"
    _rec_name = "patient_card_id"

    patient_card_id = fields.Many2one('patient.card', string="Patient card",
                                      required="True")
    # patient_id=fields.Char(related='patient_card_id.patient_id')
    name_id = fields.Many2one("res.partner",
                              related='patient_card_id.partner_id',
                              string='Patient Name')

    consultation_type = fields.Selection([
        ('Op', 'OP'),
        ('Ip', 'IP'), ],
        string='Consultation Type')

    def add_doctor(self):
        """Add data to the excisting module-job position:Doctor"""
        return [
            ('job_id', '=', self.env.ref('hospital.doctor_job_position').id)]

    doctor_id = fields.Many2one('hr.employee', string='Doctor',
                                domain=add_doctor, required="True")
    department_id = fields.Many2one(related="doctor_id.department_id",
                                    string="Department")
    date = fields.Date(string='Date', default=lambda self: fields.Date.today())
    disease = fields.Many2one("disease", string="Diseases")
    diagnose = fields.Text(string="Diagnose")
    treatment_ids = fields.One2many('patient.treatment', 'consultation_id',
                                    string="Treatment")
