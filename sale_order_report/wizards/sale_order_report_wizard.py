# -*- coding: utf-8 -*-
"""adding  filters in wizard to generate the sale report"""
from odoo import fields, models


class SalesOrderReportWizard(models.TransientModel):
    # string
    _name = 'sales.order.report.wizard'
    _description = 'Sales Order Report Wizard'

    start_date = fields.Date(string='Start Date',
                             help="Enter the the start date")
    end_date = fields.Date(string='End Date', help='Enter the end date')
    customer_id = fields.Many2one('res.partner',
                                  string='Customers',
                                  help="provide the customer name to "
                                       "generate the report based on "
                                       "the customer's sale orders")
    product_id = fields.Many2one('product.product',
                                 string='Products',
                                 help="provide the product name to "
                                      "generate the report based on "
                                      "the sale orders with that product")
    category_id = fields.Many2one('product.category',
                                  string='Product Categories',
                                  help="provide the category name to "
                                       "generate the report based on "
                                       "the sale orders with that product "
                                       "category")

    def generate_report(self):
        """function for generate report button"""
        data = {
            'form_data': self.read()[0]
        }

        # Return the report template and data
        return self.env.ref(
            'sale_order_report.sale_order_report_action').with_context(
            landscape=True).report_action(self,
                                          data=data)
