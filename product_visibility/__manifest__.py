# -*- coding: utf-8 -*-
#creating a module Associated Products
{
    'name': "Product Visibility",
    'version': '16.0.1.0.0',
    'summary':"Adding associated products to the sale order line",
    'depends': ['base', 'sale_management'],
    'author': "Author Name",
    'category': 'Category',
    'description': """By enabling the boolean field "Associated products" in 
    sale order the associated products of the customer will be added to the 
    sale order line""",
    'data': [
        'views/allowed_products_view.xml',
        ]
}

