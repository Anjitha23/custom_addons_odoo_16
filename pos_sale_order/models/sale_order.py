# -*- coding: utf-8 -*-
"""model to inherit sale.order"""
from odoo import fields, models, api


class SaleOrder(models.Model):
    """declaring a class for sale.order"""
    _inherit = 'sale.order'

    pos_session_id = fields.Many2one('pos.session', string='POS Session',readonly=True)
    created_from_pos = fields.Boolean(string="Created from POS",readonly=True)

    @api.model
    def create(self, values):
        """Check if the sale order is created from a POS session"""
        if 'pos_session_id' in values and values['pos_session_id']:
            values['created_from_pos'] = True

        # Call the original create method
        order = super(SaleOrder, self).create(values)

        return order
