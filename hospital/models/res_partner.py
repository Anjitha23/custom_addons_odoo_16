# -*- coding: utf-8 -*-
"""adding new fields to existing module"""
from odoo import fields, models
class ResPartner(models.Model):
    # _name = "inherit"
    _inherit = 'res.partner'

    dob = fields.Date(string="DOB")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')],
        string='Gender')