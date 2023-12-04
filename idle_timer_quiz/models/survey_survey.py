# -*- coding: utf-8 -*-
from odoo import fields, models


class SurveySurvey(models.Model):
    """class for inherit the survey module"""
    _inherit = 'survey.survey'

    is_idle_time = fields.Boolean(string="Idle Timer", help="Enable idle timer")
    idle_duration = fields.Integer(string="Duration",
                                   help="set idle timer duration")
