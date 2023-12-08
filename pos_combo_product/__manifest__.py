# -*- coding: utf-8 -*-
{
    'name': "Pos combo product",
    'version': '16.0.1.0.0',
    'summary':'this custom app enable the option for combo product in pos',
    'depends': ['base','point_of_sale','pos_sale'],
    'author': "Swaraj R",
    'category': 'Property',
    'description': """
    this custom app enable the 
    option for combo product in pos
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/combo_config.xml',
        'views/product_common_from.xml',
    ],

    "assets":{
            "point_of_sale.assets": [
                    'pos_combo_product/static/src/js/reciept.js',
                    'pos_combo_product/static/src/xml/combo_orderline.xml',
                    'pos_combo_product/static/src/xml/combo_limit.xml',
                    'pos_combo_product/static/src/js/popup_limit.js',
                    'pos_combo_product/static/src/xml/product_pop_up.xml',
                    'pos_combo_product/static/src/js/combo_pop_up.js',
                    'pos_combo_product/static/src/js/product_click.js',
                    'pos_combo_product/static/src/css/product_item.css',
                    'pos_combo_product/static/src/xml/product_item.xml',

                ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}