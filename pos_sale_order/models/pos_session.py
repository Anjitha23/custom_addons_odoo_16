# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PosSession(models.Model):
    _inherit = 'pos.session'

    sale_order_ids = fields.One2many(
        'sale.order',
        'pos_session_id',
        string='Related Sale Orders',
        domain="[('pos_session_id', '=', id), ('created_from_pos', '=', True)]"
    )

    sale_order_count = fields.Integer(
        'Sale Order Count',
        compute='_compute_sale_order_count',
    )

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for session in self:
            session.sale_order_count = len(session.sale_order_ids)

    def action_open_sale_orders(self):
        sale_order_ids = self.sale_order_ids.ids

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('id', 'in', sale_order_ids)],
        }
