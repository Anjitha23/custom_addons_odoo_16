# -*- coding: utf-8 -*-
"""adding a field product to customers"""
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.Many2many("product.product",
                                   string="Associated Products")
