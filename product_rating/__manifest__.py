# -*- coding: utf-8 -*-
{
    'name': "Product Rating",
    'version': '16.0.1.0.0',
    'summary':"Adding associated products to the sale order line",
    'depends': ['base','point_of_sale','product'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """By enabling the boolean field "Associated products" in 
    sale order the associated products of the customer will be added to the 
    sale order line""",
    'data': [
        'views/product_rating_view.xml',
        ],
    'assets': {
       'point_of_sale.assets': [
            'product_rating/static/src/js/product_rating_receipt.js',
           'product_rating/static/src/xml/custom_pos_rating.xml',
       ],
    }
}


