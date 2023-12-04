# -*- coding: utf-8 -*-
"""Employee Ticket table"""
from odoo import api, fields, models, _


class EmployeeTicket(models.Model):
    """employee ticket model"""
    _name = "employee.ticket"
    _description = "Employee Ticket"
    _inherit = 'mail.thread'
    _rec_name = 'ticket'

    ticket = fields.Char(string='Ticket_no:', readonly=True,
                         default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id = fields.Many2one('res.users', related='employee_id.user_id',
                              string='User')
    date = fields.Date(string='Date', default=lambda self: fields.Date.today())
    hr_related_requests = fields.Text(string="HR related requests")
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'),
         ('approved', 'Approved'), ('rejected', 'Rejected')],
        string='State', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('ticket', _('New')) == _('New'):
            vals['ticket'] = self.env['ir.sequence'].next_by_code(
                'employee.ticket') or _('New')
        return super(EmployeeTicket, self).create(vals)

    def action_submit(self):
        """function for submit button"""
        self.write({'state': "submit"})

    def action_approve(self):
        """function for approve button"""
        self.write({'state': "approved"})

    def action_reject(self):
        """function for reject button"""
        self.write({'state': "rejected"})
