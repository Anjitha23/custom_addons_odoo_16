# -*- coding: utf-8 -*-
"""patient OP table"""

from odoo import api, fields, models


class PatientOp(models.Model):
    """patient op model"""
    _name = "patient.op"
    _description = "Patient Op"
    _inherit = "mail.thread"
    _rec_name = "patient_card_id"

    patient_card_id = fields.Many2one('patient.card', string="Patient card",
                                      required="True")
    appointment_id = fields.Many2one('dr.appointment', store=True)
    name_id = fields.Many2one("res.partner",
                              related='patient_card_id.partner_id',
                              string='Patient Name')

    age = fields.Integer(string='Age', related='patient_card_id.age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')],
        string='Gender', related='patient_card_id.gender')
    blood_group = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')],
        string='Blood Group', related='patient_card_id.blood_group')

    def add_doctor(self):
        """Add data to the existing module-job position: Doctor"""
        return [
            ('job_id', '=',
             self.env.ref('hospital.doctor_job_position').id)
        ]

    doctor_id = fields.Many2one('hr.employee', string='Doctor', required="True",
                                domain=add_doctor)

    date = fields.Date(string='Date', default=lambda self: fields.Date.today())
    token = fields.Integer(string="Token No", compute='_compute_token',
                           store=True)
    new_token = fields.Integer(compute='regenerate_tokens')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    fee = fields.Monetary(related="doctor_id.fee", string="Fee")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], string='Status', tracking=True, default='draft')
    pay_id = fields.Many2one('account.move', string="Payment")
    ribbon = fields.Boolean(compute='_compute_ribbon')

    def _compute_ribbon(self):
        """function to get paid ribbon in smart bar"""
        if self.pay_id.payment_state == 'paid':
            self.state = 'paid'
            self.ribbon = True
        else:
            self.ribbon = False

    def action_confirm(self):
        """function for confirm button"""
        self.write({'state': "confirm"})

    def action_payment(self):
        """ Create the product 'OP Ticket' if it doesn't exist"""
        ticket_id = self.env['product.product'].search(
            [('name', '=', 'OP Ticket')], limit=1)
        if not ticket_id:
            ticket_id = self.env['product.product'].create({
                'name': 'OP Ticket',
                'type': 'service',
                'list_price': self.fee,
                'standard_price': self.fee,
            })
        # Create a payment record linked to the patient.op
        payment = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.name_id.id,
            'doctor_id': self.doctor_id.id,
            'invoice_date': self.date,
            'invoice_line_ids': [(0, None, {
                'product_id': ticket_id.id,
                'name': self.patient_card_id.name,
                'quantity': 1,
                'price_unit': self.fee,
            })],
        })
        self.pay_id = payment.id
        self.pay_id.action_post()

        # Mark the record as paid
        self.write({'state': 'paid'})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.pay_id.id,
        }

    def get_payment(self):
        """function for get the smart button of payments"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.pay_id.id,
            'target': 'new'
        }

    @api.depends('doctor_id', 'date')
    def _compute_token(self):
        """Generate and regenerate token numbers"""
        for record in self:
            if record.doctor_id and record.date:
                domain = [
                    ('doctor_id', '=', record.doctor_id.id),
                    ('date', '=', record.date)
                ]
                record.token = self.search_count(domain)

    @api.model
    def regenerate_tokens(self):
        """Regenerate tokens for all records"""
        all_records = self.search([])
        for record in all_records:
            domain = [
                ('doctor_id', '=', record.doctor_id.id),
                ('date', '=', record.date)
            ]
            token_count = self.search_count(domain)
            record.write({'token': token_count + 1})
