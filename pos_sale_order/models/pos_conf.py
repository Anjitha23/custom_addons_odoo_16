# -*- coding: utf-8 -*-
"""adding a discount tag field  to product form"""
from odoo import fields, models


class PosConfiguration(models.Model):
    """class to inherit the pos.config"""
    _inherit = 'pos.config'

    create_sale_order = fields.Boolean(
        string='Create Sale Order',
        help="Enable this to create sale order from pos product screen")


class ResConfSettings(models.TransientModel):
    """class to inherit the res.config.settings"""
    _inherit = 'res.config.settings'

    create_sale_order = fields.Boolean(
        related="pos_config_id.create_sale_order",
        string='Create Sale Order',
        help="Enable this to create sale order from pos product screen",
        readonly=False)
