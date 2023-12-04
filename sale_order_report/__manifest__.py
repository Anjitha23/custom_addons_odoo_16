# -*- coding: utf-8 -*-
{
    'name': "Sale Order Report",
    'version': '16.0.6.0.0',
    'depends': ['base', 'sale_management'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """Generate report for the sale order""",
    'data': [
        'security/ir.model.access.csv',
        'report/sale_order_report_action.xml',
        'report/report_template.xml',
        'wizards/sale_order_report_wizard_view.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
