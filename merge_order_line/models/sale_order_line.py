# -*- coding: utf-8 -*-
"""inheriting the sale order module"""
from odoo import api, models


class SaleOrderInherit(models.Model):
    """Class for inheriting the sale order"""

    _inherit = 'sale.order'

    def merge_order_lines(self):
        """It checks whether the product ids and unit price of the products
                 are same or not in line by line"""
        line_ids = {}
        for line in self.order_line:
            key = (line.product_id.id, line.price_unit, line.product_uom)
            if key in line_ids:
                line_ids[key] += line.product_uom_qty

            else:
                line_ids[key] = line.product_uom_qty

        self.order_line.unlink()


        for (product_id, price_unit, product_uom), qty in line_ids.items():
            self.env['sale.order.line'].create({
                'order_id': self.id,
                'product_id': product_id,
                'price_unit': price_unit,
                'product_uom':product_uom.id,
                'product_uom_qty': qty,
            })

    @api.model
    def create(self, vals):
        """merge the order line when customer create the sale order"""
        res = super(SaleOrderInherit, self).create(vals)
        res.merge_order_lines()
        return res

    def action_confirm(self):

        self.merge_order_lines()
        return super(SaleOrderInherit, self).action_confirm()
