# -*- coding: utf-8 -*-
"""Inheriting pos_session model"""
from odoo import api, fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    # Add a One2many field to store related sale orders
    sale_order_ids = fields.One2many('sale.order',
                                     'pos_session_id',
                                     string='Related Sale Orders')
    sale_order_count = fields.Integer('Sale Order Count',
                                      compute='_compute_sale_order_count',
                                      store=True)

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for session in self:
            session.sale_order_count = len(session.sale_order_ids)

    def action_open_sale_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': self.sale_order_ids.id
        }
