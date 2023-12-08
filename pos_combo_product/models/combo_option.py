# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ComboConfiguration(models.Model):
    _name = 'combo.configuration'
    _description = 'this model represents the configuration of the product'

    combo_pos_category_id = fields.Many2one('pos.category', string='Pos category', help='pos category selection field', required=True)
    combo_product_ids = fields.Many2many('product.product', string='Combo products', required=True,
                                         domain="[('pos_categ_id', '=', combo_pos_category_id)]",
                                         help='choose specific product')
    is_required_product = fields.Boolean(string='Is required', help='weather this product is a required one')
    item_count = fields.Integer(string='Item count', help='Item count of the selected products', default=1)
    product_template_id = fields.Many2one('product.product')

    @api.onchange('combo_pos_category_id')
    def category_change(self):
        """function to set dynamically domain to field combo_pos_category_id to avoid occurrence"""
        category_id =self.product_template_id.combo_options_ids.mapped('combo_pos_category_id.id')
        domain = [('id', 'not in', category_id)]
        return {'domain': {'combo_pos_category_id': domain}}






