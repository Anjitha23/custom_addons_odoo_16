# -*- coding: utf-8 -*-
"""adding a field product to customers"""
from odoo import fields, models


class ResPartner(models.Model):
    """class to inherit existing model"""
    _inherit = 'res.partner'

    is_purchase_limit = fields.Boolean(
        string="Activate Purchase Limit",
        help="If you enable this field,Purchase "
             "Limit customer can add purchase limit")
    add_limit = fields.Monetary(
        string="Purchase Limit Amount",
        help=("customer can add the purchase limit amount"))


class PosSession(models.Model):
    """class to inherit pos_session"""
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        """function to load data in pos"""
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend(['add_limit',
                                                  'is_purchase_limit'])
        return result
