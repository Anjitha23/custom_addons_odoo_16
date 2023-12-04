# -*- coding: utf-8 -*-
"""adding a field associated product to sale_orders"""
from odoo import api, fields, models


class SaleOrder(models.Model):
    """New class to inherit the sale order"""
    _inherit = 'sale.order'

    associated_products = fields.Boolean(string="Associated Products",
                                         help="If you enable this field,"
                                              "Associated products"
                                              " of the customer will be"
                                              " added to the order line")

    @api.onchange('associated_products')
    def onchange_associated_products(self):
        """If associated_products is disabled, remove associated
                            products from order lines"""
        if not self.associated_products:
            to_disable = []
            for line in self.order_line:
                if line.product_id in self.partner_id.product_ids:
                    to_disable.append((3, line.id, 0))
            self.order_line = to_disable
        else:
            if self.partner_id:
                order_line_vals = [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 1,
                }) for product in self.partner_id.product_ids]
                self.order_line = order_line_vals
