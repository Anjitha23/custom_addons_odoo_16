# -*- coding: utf-8 -*-
{
    'name': "POS Sale Order",
    'version': '16.0.1.0.0',
    'summary':"Adding Sale order buttom to the product screen in Point of sale",
    'depends': ['base','point_of_sale'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """Adding a sale order button to the product screen in point of sale to create sale order in sale order module """,
    'data': [
        'views/pos_config_views.xml',
        'views/pos_session.xml',
        ],
    'assets': {
       'point_of_sale.assets': [
            'pos_sale_order/static/src/js/sale_order_button.js',
           # 'pos_sale_order/static/src/js/sale_order_popup.js',
           'pos_sale_order/static/src/xml/sale_order_btn.xml',
           # 'pos_sale_order/static/src/xml/sale_order_popup.xml'
       ],
    }
}


