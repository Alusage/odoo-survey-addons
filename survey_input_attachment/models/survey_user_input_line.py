# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _

ANSWER_TYPES = [
    ("text", _("Text")),
    ("number", _("Number")),
    ("date", _("Date")),
    ("free_text", _("Free Text")),
    ("upload_file", _("Attachment (img/pdf)")),
    ("suggestion", _("Suggestion")),
]

FILE_TYPES = [
    ("image", _("Image")),
    ("pdf", _("PDF file")),
]


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input_line"

    answer_type = fields.Selection(selection=ANSWER_TYPES)
    file = fields.Binary(string="Uploaded file")
    filename = fields.Char(string="Uploaded file name")
    file_type = fields.Selection(selection=FILE_TYPES, string="File type")

    @api.model
    def save_line_upload_file(self, user_input_id, question, post, answer_tag):
        vals = {
            "user_input_id": user_input_id,
            "question_id": question.id,
            "survey_id": question.survey_id.id,
            "skipped": False,
        }
        file = False
        # import ipdb; ipdb.set_trace()
        if question.constr_mandatory:
            file = base64.encodebytes(post[answer_tag].read())
        else:
            file = (
                base64.encodebytes(post[answer_tag].read())
                if not isinstance(post[answer_tag], str)
                else None
            )
        if answer_tag in post and not isinstance(post[answer_tag], str):
            vals.update(
                {
                    "answer_type": "upload_file",
                    "file": file,
                    "filename": post[answer_tag].filename,
                }
            )
            if post[answer_tag].content_type == "application/pdf":
                vals.update({"file_type": "pdf"})
            if "image/" in post[answer_tag].content_type:
                vals.update({"file_type": "image"})
        else:
            vals.update(
                {
                    "answer_type": None,
                    "file": False,
                    "filename": False,
                    "skipped": True,
                }
            )
        old_uil = self.search(
            [
                ("user_input_id", "=", user_input_id),
                ("survey_id", "=", question.survey_id.id),
                ("question_id", "=", question.id),
            ]
        )
        if old_uil:
            old_uil.write(vals)
        else:
            old_uil.create(vals)
        return True
