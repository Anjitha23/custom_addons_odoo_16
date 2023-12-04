# -*- coding: utf-8 -*-
{
    'name': "Material Request",
    'version': '16.0.1.0.0',
    'depends': ['base', 'hr', 'product', 'purchase', 'stock'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/material_req_sequence.xml',
        'views/material_request_menu.xml',
        'views/material_request_views.xml',
        'views/request_product_views.xml',
        'views/purchase_order_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable': True,
}
