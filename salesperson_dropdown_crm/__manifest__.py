# -*- coding: utf-8 -*-
{
    'name': "Salesperson Dropdown",
    'version': '16.0.6.0.0',
    'depends': ['base', 'crm'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """When change the salesperson from the dropdown menu,it will affect the filter and display the tree view""",
    'data': [
        'views/crm_lead_tree_views.xml',
    ],
    'assets': {
        "web.assets_backend": [
            'salesperson_dropdown_crm/static/src/js/salesperson_crm_lead.js',
            'salesperson_dropdown_crm/static/src/xml/salesperson_crm_lead_views.xml',
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
