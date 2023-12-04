# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'version': '16.0.6.0.0',
    'depends': ['base', 'sale_management', 'hr', 'account','website'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """
    Description text
    """,
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/doctor.xml',
        'data/disease.xml',
        'data/book_appointment_data.xml',
        'report/patient_report.xml',
        'report/patient_report_template.xml',
        'views/hospital_view.xml',
        'wizards/medical_report_views.xml',
        'views/hospital_menu.xml',
        'views/hospital_op_menu.xml',
        'views/hospital_op_view.xml',
        'views/res_partner.xml',
        'views/consultation_menu.xml',
        'views/consultation_view.xml',
        'views/treatment_view.xml',
        'views/hr_employee.xml',
        'views/dr_appointment_view.xml',
        'views/account_move.xml',
        'wizards/create_appointment_view.xml',
        'views/appointment_webpage.xml',
        'views/patient_card_webpage.xml',
        'views/snippets/doctor_snippet_view.xml',
        'views/doctor_details.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'hospital/static/src/js/action_xls.js',
        ],
        'web.assets_frontend':[
            'hospital/static/src/xml/doctor_template.xml',
            'hospital/static/src/js/patient_details.js',
            'hospital/static/src/js/doctor_snippets.js',
        ]
    },
}
