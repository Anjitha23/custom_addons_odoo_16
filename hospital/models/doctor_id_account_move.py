# -*- coding: utf-8 -*-
""" Adding field doctor in existin modele account.move"""

from odoo import fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    doctor_id = fields.Many2one('hr.employee', string='Doctor')
