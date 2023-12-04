# -*- coding: utf-8 -*-
"""Daily Work Report table"""
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class DailyWorkReport(models.Model):
    _name = 'daily.work.report'
    _inherit = 'mail.thread'
    _description = 'Daily Work Report'

    name = fields.Char(string='Report Title', readonly=True)
    employee = fields.Char(string='Employee', readonly=True)
    date = fields.Date(string='Date', default=lambda self: fields.Date.today(), readonly=True)
    email_body = fields.Html(string='Email Body', readonly=True)

    @api.model
    def get_daily_report_count(self, selected_date=None):
        domain = [('date', '=', selected_date)] if selected_date else []

        total_employees = self.env['hr.employee'].search_count([])
        employees_with_email = self.search_count(domain + [('email_body', '!=', False)])
        employees_without_email = total_employees - employees_with_email

        data = {
            'total_employees': total_employees,
            'employees_with_email': employees_with_email,
            'employees_without_email': employees_without_email,
        }

        return data

    @api.model
    def get_daily_report_data(self, selected_date):
        domain = [('date', '=', selected_date), ('email_body', '!=', False)]
        reports = self.search(domain)
        data = [{'report_key': report.id, 'name': report.name, 'employee': report.employee} for report in reports]

        return data
