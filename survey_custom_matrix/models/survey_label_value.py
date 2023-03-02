# -*- coding: utf-8 -*-
from odoo import models, fields


class SurveyLabelValue(models.Model):
    _name = "survey.label.value"
    _description = "Value"

    name = fields.Char(string="Name")
