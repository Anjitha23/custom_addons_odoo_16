# -*- coding: utf-8 -*-
"""adding new fields to existing module"""
from odoo import fields, models


class ProductAverageCost(models.Model):
    """inheriting product_template model into new model"""
    _inherit = 'product.template'

    product_average_cost = fields.Float(compute='_compute_average_cost',
                                        string="Average Cost")

    def _compute_average_cost(self):
        """function to compute the average product cost"""
        purchase_order = self.env['purchase.order.line']
        for product_template in self:
            # Accessing product.product records associated with the template
            product_products = product_template.product_variant_ids
            # Calculate the total cost and number of products
            total_cost = 0.0
            total_qty = 0.0
            for product_product in product_products:
                purchase_orders = purchase_order.search(
                    [('product_id', '=', product_product.id)])
                total_cost += sum(
                    order.price_subtotal for order in purchase_orders)
                total_qty += sum(order.product_qty for order in purchase_orders)
            average_cost = total_cost / total_qty if total_qty > 0 else 0.0
            product_template.write({'product_average_cost': average_cost})
