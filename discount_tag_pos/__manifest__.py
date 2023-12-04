# -*- coding: utf-8 -*-
#creating a module Associated Products
{
    'name': "Discount Tag ",
    'version': '16.0.1.0.0',
    'summary':"Discount price tag in the POs Screen in the product view ",
    'depends': ['base', 'point_of_sale'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """ show the Discount price tag in the POs 
    Screen in the product view as small icon on the top right
     corner and in receipt.""",
    'data': [
        'views/discount_tag_view.xml',
        ],
    'assets': {
            'point_of_sale.assets': [
                'discount_tag_pos/static/src/js/discount_price_receipt.js',
                 'discount_tag_pos/static/src/xml/pos_discount_tag.xml',
            ],
    }
}


