{
    'name': "Razorpay Payment",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Razorpay Payment Provider',
    'description': """
     Razorpay Payment Provider.
    """,
    'depends' : [
        'website',
        'payment',

    ],
    'data': [
        'views/razorpayment_provider_view.xml',
        'views/razorpayment_templates.xml',
        'data/razorpayment_data_view.xml'
    ],
}