# -*- coding: utf-8 -*-
"""adding a discount tag field  to product form"""
from odoo import fields, models


class ComboProduct(models.Model):
    """class to inherit the product_product"""
    _inherit = 'product.template'

    is_combo = fields.Boolean(
        string='Allow Combo Products', help="Add Combo Products")

    product_ids = fields.Many2many('product.product',string='combo products')
