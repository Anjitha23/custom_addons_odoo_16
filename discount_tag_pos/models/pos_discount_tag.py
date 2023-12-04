# -*- coding: utf-8 -*-
"""adding a priority field product to product form"""
from odoo import models


class PosSession(models.Model):
    """class to inherit pos session"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """function to load data in pos"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['discount_price'])
        return result
