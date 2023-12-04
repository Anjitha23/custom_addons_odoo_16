# -*- coding: utf-8 -*-
#creating a module Associated Products
{
    'name': "Purchase Limit",
    'version': '16.0.1.0.0',
    'summary':"Adding purchase limit to the customer",
    'depends': ['base', 'point_of_sale'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """By enabling the boolean field "Purchase Limit" in 
    point of sale the Purchase Limit of the customer can  add limit 
    """,
    'data': [
        'views/purchase_limit_views.xml',
        ],
    'assets': {
            'point_of_sale.assets': [
                'purchase_limit_pos/static/src/js/limit_popup.js',
                 'purchase_limit_pos/static/src/xml/limit_in_tree_view.xml',
            ],
    }
}
