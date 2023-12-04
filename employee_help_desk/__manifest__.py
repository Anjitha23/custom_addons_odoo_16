# -*- coding: utf-8 -*-
{
    'name': "Employee Help Desk",
    'version': '16.0.1.0.0',
    'summary':"Generating employee ticket through website",
    'depends': ['base','hr','website'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """employee can raise help desk ticket through website for
     different kinds of HR related requests in your company,
     Allow your Employee Manager to view all tickets and 
     process and action on support tickets""",
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/website_ticket_menu.xml',
        'views/employee_ticket_menu.xml',
        'views/employee_ticket_view.xml',
        'views/employee_ticket_webpage.xml'
        ]
}
