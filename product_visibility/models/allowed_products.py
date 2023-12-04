# -*- coding: utf-8 -*-
"""adding a field product to customers"""
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_allowed_products = fields.Boolean(string="Allowed Products",
                                         help="If you enable this field,"
                                              "Allowed products"
                                              " of the customer will be"
                                              " added to the shop")
    allowed_product_ids = fields.Many2many("product.template",
                                           string="Products")
    allowed_category_ids = fields.Many2many("product.category",
                                            string="Product Categories")
