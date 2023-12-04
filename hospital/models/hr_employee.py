# -*- coding: utf-8 -*-
"""adding new fields to existing module"""

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    fee = fields.Monetary(string="Fee")
    is_doctor = fields.Boolean('Is Doctor')

    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id.name == 'Doctor':
            self.is_doctor = True
        else:
            self.is_doctor = False
