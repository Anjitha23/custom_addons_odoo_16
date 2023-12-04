# -*- coding: utf-8 -*-
"""Add in datas for diseases"""

from odoo import fields, models


class Disease(models.Model):
    """disease model"""
    _name = "disease"
    _description = "Diseases"

    name = fields.Char(string="Diseases")
