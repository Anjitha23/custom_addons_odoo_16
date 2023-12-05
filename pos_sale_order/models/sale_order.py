# -*- coding: utf-8 -*-
"""Inheriting sale_order model"""
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Add a Many2one field to link to POS session
    pos_session_id = fields.Many2one('pos.session', string='POS Session')