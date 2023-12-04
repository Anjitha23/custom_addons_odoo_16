# -*- coding: utf-8 -*-
"""adding a field to relate two models"""

from odoo import fields, models


class StockPickingInherit(models.Model):

    _inherit = 'stock.picking'
    internal_transfer_id = fields.Many2one("material.request")

    def get_internal_request(self):
        """function for get the smart button of purchase orders"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Material Request',
            'view_mode': 'form',
            'res_model': 'material.request',
            'res_id':self.internal_transfer_id.id
        }
