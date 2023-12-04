{
    'name': "Website Theme",
    'version': '16.0.1.0.0',
    'depends': ['base','website'],
    'author': "Anjitha",
    'category': 'Theme',
    'description': """
    Description text
    """,
    'data':
    [
        'data/pages/menu.xml',
        'data/pages/about_us.xml',

    ],
    'assets':{
        'web._assets_primary_variables':[
            '/website_theme/static/scss/primary_variables.scss'
        ],
    },
    'images':
        [
        'static/description/clean_description.jpg',
        'static/description/clean_screenshot.jpg'
            ]

}