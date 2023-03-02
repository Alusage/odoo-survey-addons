# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from werkzeug.datastructures import FileStorage

TYPES = [
    ("free_text", _("Multiple Lines Text Box")),
    ("textbox", _("Single Line Text Box")),
    ("numerical_box", _("Numerical Value")),
    ("date", _("Date")),
    ("upload_file", _("Attachment (img/pdf)")),
    ("simple_choice", _("Multiple choice: only one answer")),
    ("multiple_choice", _("Multiple choice: multiple answers allowed")),
    ("matrix", _("Matrix")),
]


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    # question_attachment = fields.Binary(string="Joined attachment")
    type = fields.Selection(selection=TYPES)

    @api.multi
    def validate_upload_file(self, post, answer_tag):
        self.ensure_one()
        errors = {}
        # Empty answer to mandatory question
        if self.constr_mandatory and not isinstance(post[answer_tag], FileStorage):
            errors.update({answer_tag: self.constr_error_msg})
        # Bad file type
        if (
            isinstance(post[answer_tag], FileStorage)
            and post[answer_tag].content_type != "application/pdf"
            and "image/" not in post[answer_tag].content_type
        ):
            errors.update(
                {answer_tag: _("The file you joined is not an image nor a PDF file.")}
            )
        return errors
