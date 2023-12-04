# -*- coding: utf-8 -*-
"""adding a field product to manufacturing"""
from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    customer_id = fields.Many2one('res.partner',string='Customer')
