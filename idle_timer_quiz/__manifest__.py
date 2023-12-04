# -*- coding: utf-8 -*-
{
    'name': "Quiz-idle Timer",
    'version': '16.0.1.0.0',
    'summary':"Set idle timer for quiz",
    'depends': ['base','survey','website'],
    'author': "Anjitha",
    'category': 'Category',
    'description': """If mouse and keyboard are idle 
    for a particular time,  timer should start 
    After a particular time it should move to next page.""",
    'data': [
        'views/idle_timer_view.xml',
        'views/survey_templates.xml'
        ],
    'assets': {
        'web.assets_frontend':[
                'idle_timer_quiz/static/src/js/idle_timer_countdown.js',
            ]
    }
}
