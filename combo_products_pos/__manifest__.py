# -*- coding: utf-8 -*-
{
    'name': "Combo Products",
    'version': '16.0.1.0.0',
    'summary':"Adding combo products to thePoint of sale",
    'depends': ['base','point_of_sale','product'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """By enabling the boolean field "Combo Products" in 
    point of sale the combo products of the product will be added to the 
    pos product line""",
    'data': [
        'views/product_template_view.xml',
        ],
    'assets': {
       'point_of_sale.assets': [
           #  'product_rating/static/src/js[ /product_rating_receipt.js',
           'combo_products_pos/static/combo_tag_template_view.xml',
       ],
    }
}


