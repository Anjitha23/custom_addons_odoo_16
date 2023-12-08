# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'inherited product.product to add is combo options'

    combo_ok = fields.Boolean(string="Is combo", help='boolean field to check weather the product is combo')
    combo_options_ids = fields.One2many('combo.configuration', 'product_template_id')

    @api.model
    def get_combo_product(self, args):
        """get product combo details"""
        combo_products = self.env['combo.configuration'].search([('id', 'in', args)])
        product_list = []
        for each in combo_products:
            values = {
                'id': each.id,
                'pos_category': each.combo_pos_category_id.name,
                'is_required': each.is_required_product,
                'item_count': each.item_count,
            }
            vals = []
            for product in each.combo_product_ids:
                value = {
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_image': product.image_1920,
                    'max_count': each.item_count,
                    'pos_category': each.combo_pos_category_id.name,
                }
                vals.append(value)
            values['products'] = vals
            product_list.append(values)
        return product_list

    class PosSession(models.Model):
        """inherited pos.session to load the fields from product.product"""
        _inherit = 'pos.session'

        def _loader_params_product_product(self):
            """function to load field to pos"""
            result = super()._loader_params_product_product()
            result['search_params']['fields'].extend(['combo_options_ids', 'combo_ok'])
            return result
