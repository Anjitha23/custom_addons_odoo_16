# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError

class SaleOrderReport(models.AbstractModel):
    _name = "report.sale_order_report.report_sale_order"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sales.order.report.wizard'].browse(docids)

        start_date = data['form_data'].get('start_date', False)
        end_date = data['form_data'].get('end_date', False)
        customer_id = data['form_data'].get('customer_id', False)
        product_id = data['form_data'].get('product_id', False)
        category_id = data['form_data'].get('category_id', False)

        query = """
            SELECT
                to_char(so.date_order, 'DD-MM-YYYY HH:MM') AS sale_order_date,
                pt.name AS product_name,
                pt.list_price AS list_price,
                sol.product_uom_qty AS quantity,
                sol.product_uom AS product_uom_id,
                uom.name::json->'en_US' AS product_uom_name,
                sol.price_reduce_taxexcl AS price_reduce_taxexcl,
                sol.price_reduce_taxinc AS price_reduce_taxinc,
                sol.price_subtotal AS price_subtotal,
                pc.name AS product_category,
                res_partner.name AS customer_name,
                so.amount_total AS order_total
            FROM
                sale_order so
            JOIN
                sale_order_line sol ON so.id = sol.order_id
            JOIN
                product_product pp ON sol.product_id = pp.id
            JOIN
                product_template pt ON pp.product_tmpl_id = pt.id
            JOIN
                product_category pc ON pt.categ_id = pc.id
        
            LEFT JOIN
                uom_uom uom ON sol.product_uom = uom.id
            JOIN
                res_partner ON so.partner_id = res_partner.id
        """

        conditions = []

        if start_date:
            conditions.append(f"so.date_order >= '{start_date}'")

        if end_date:
            conditions.append(f"so.date_order <= '{end_date}'")

        if customer_id:
            customer_id = customer_id[0]
            query += f" AND so.partner_id = '{customer_id}'"

        if product_id:
            product_id = product_id[0]
            conditions.append(f"pp.id = {product_id}")

        if category_id:
            category_id = category_id[0]
            conditions.append(f"pt.categ_id = {category_id}")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY so.date_order DESC"

        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()

        if not result:
            raise UserError(_("No sale orders found for the given filters."))

        return {
            'doc_ids': docids,
            'doc_model': 'sales.order.report.wizard',
            'docs': docs,
            'data': data,
            'currency': self.env.user.company_id.currency_id,
            'sale_orders': result,
        }
