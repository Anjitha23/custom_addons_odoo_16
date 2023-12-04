# -*- coding: utf-8 -*-
"""Patient treatment table"""
from odoo import fields, models


class PatientTreatment(models.Model):
    _name = 'patient.treatment'
    _description = 'Treatment'

    consultation_id = fields.Many2one('consultation', string='Consultation')
    medicine = fields.Char(string='Medicine')
    dose = fields.Char(string='Dose')
    days = fields.Integer(string='Days')
    description = fields.Text(string='Description')
