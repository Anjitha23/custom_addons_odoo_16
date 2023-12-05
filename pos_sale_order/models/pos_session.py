# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PosSession(models.Model):
    _inherit = 'pos.session'

    sale_order_ids = fields.One2many(
        'sale.order',
        'pos_session_id',
        string='Related Sale Orders',
        domain="[('pos_session_id', '=', id)]"
    )

    sale_order_count = fields.Integer(
        'Sale Order Count',
        compute='_compute_sale_order_count',
        store=True
    )
    print("hii")

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        print('helo')
        for session in self:
            print(session)
            session.sale_order_count = len(session.sale_order_ids.filtered(lambda so: so.pos_session_id == session))
            print(session.sale_order_count)

    def action_open_sale_orders(self):
        # Get the IDs of sale orders related to the current POS session
        sale_order_ids = self.sale_order_ids.ids

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('id', 'in', sale_order_ids)],
        }
