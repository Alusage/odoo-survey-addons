# -*- coding: utf-8 -*-
from odoo import models, fields

TYPES = [
    ("free_text", "Multiple Lines Text Box"),
    ("textbox", "Single Line Text Box"),
    ("numerical_box", "Numerical Value"),
    # ('date', 'Date'),
    ("dropdown", "Dropdown"),
    ("checkbox", "Checkbox"),
]


class SurveyLabel(models.Model):
    _inherit = "survey.label"

    type = fields.Selection(
        selection=TYPES, string="Type of question", default="checkbox", required=True
    )
    value_ids = fields.Many2many(comodel_name="survey.label.value", string="Values")
