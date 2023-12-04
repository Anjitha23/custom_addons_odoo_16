# -*- coding: utf-8 -*-
"""adding a field to relate two models"""

from odoo import fields, models


class PurchaseOrderInherit(models.Model):

    _inherit = 'purchase.order'
    material_request_id = fields.Many2one("material.request")

    def get_material_request(self):
        """function for get the smart button of purchase orders"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Material Request',
            'view_mode': 'form',
            'res_model': 'material.request',
            'res_id':self.material_request_id.id
        }
