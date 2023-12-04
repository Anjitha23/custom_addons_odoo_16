# -*- coding: utf-8 -*-
"""adding a priority field product to product form"""
from odoo import fields, models


class ProductRating(models.Model):
    _inherit = 'product.product'

    product_rating = fields.Selection(
        [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'),
         ('4', '4'),('5','5')],
        string='Quality Rate')
class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):

        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['product_rating'])
        return result
