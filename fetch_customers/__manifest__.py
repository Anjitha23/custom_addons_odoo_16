# -*- coding: utf-8 -*-
{
    'name': "Fetch Customers",
    'version': '16.0.1.0.0',
    'summary':"Transferng customers from odoo15 to odoo16",
    'depends': ['base','contacts'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """client is shifting from odoo15 to odoo16 he need to transfer customers from odoo15 to odoo16""",
    'data': [
        'security/ir.model.access.csv',
        'wizard/transfer_data_wizard_view.xml'
        ]
}

