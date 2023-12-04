# -*- coding: utf-8 -*-
"""adding a discount tag field  to product form"""
from odoo import fields, models


class ProductRating(models.Model):
    """class to inherit the product_product"""
    _inherit = 'product.product'

    discount_price = fields.Monetary(
        string='Discount Price', help="Add discount price here")
