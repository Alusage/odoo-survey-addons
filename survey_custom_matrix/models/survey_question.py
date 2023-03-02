# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.addons.survey.models.survey import dict_keys_startswith


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    matrix_subtype = fields.Selection(
        selection_add=[("custom", "Custom Matrix")],
        required=True,
    )

    @api.onchange("matrix_subtype")
    def onchange_matrix_subtype(self):
        self.ensure_one()
        if self.matrix_subtype != "custom":
            labels = self.labels_ids
            labels.filtered(
                lambda label: label.type not in ["checkbox", "dropdown"]
            ).update({"type": "checkbox"})
            labels.filtered(lambda label: label.type == "dropdown").update(
                {"type": "checkbox", "value_ids": [(5)]}
            )

    @api.multi
    def validate_matrix(self, post, answer_tag):
        self.ensure_one()
        errors = {}
        if self.constr_mandatory:
            lines_number = len(self.labels_ids_2)
            answer_candidates = dict_keys_startswith(post, answer_tag)
            answer_candidates.pop(("%s_%s" % (answer_tag, "comment")), "").strip()
            # Number of lines that have been answered
            if self.matrix_subtype == "simple":
                answer_number = len(answer_candidates)
            elif self.matrix_subtype == "multiple":
                answer_number = len({sk.rsplit("_", 1)[0] for sk in answer_candidates})
            elif self.matrix_subtype == "custom":
                answer_number = len({sk.rsplit("_", 1)[0] for sk in answer_candidates})
            else:
                raise RuntimeError("Invalid matrix subtype")
            # Validate that each line has been answered
            if answer_number != lines_number:
                errors.update({answer_tag: self.constr_error_msg})
        return errors
