# -*- coding: utf-8 -*-
{
    'name': "Employee Daily Work Report Tracker",
    'version': '16.0.1.0.0',
    'summary': "Generating employee daily work report",
    'depends': ['base', 'hr', 'website'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """employee can sumbit their daily work report""",
    'data': [
        'security/ir.model.access.csv',
        'views/daily_work_report_menu.xml',
        'views/daily_work_report_view.xml',
    ],
    'assets': {
        "web.assets_backend": [
            'employee_work_report/static/src/dashboard/work_report_dashboard.xml',
            'employee_work_report/static/src/dashboard/work_report_dashboard.js',
        ]
    }
}
