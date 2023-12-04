# -*- coding: utf-8 -*-
"""Product Request Table"""
from odoo import models, fields


class RequestProduct(models.Model):
    """class for product request"""
    _name = 'request.product'

    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    quantity = fields.Float(string='Quantity', default=1)
    request_id = fields.Many2one(
        'material.request', string='Material Request')
    location_id = fields.Many2one('stock.location', string='Source location')
    location_dest_id = fields.Many2one('stock.location',
                                       string="Destination location")
    delivery_method = fields.Selection(
        [('po', 'Purchase Order'), ('it', 'Internal Transfer')],
        string='Delivery Method', required=True)
