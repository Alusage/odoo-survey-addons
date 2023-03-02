# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.survey.models.survey import dict_keys_startswith


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input_line"

    answer_type = fields.Selection(
        selection_add=[("dropdown", "Dropdown")], string="Answer Type"
    )
    matrix_subtype = fields.Selection(related="question_id.matrix_subtype")
    value_id = fields.Many2one("survey.label.value", string="Value Dropdown")

    @api.model
    def save_line_matrix(self, user_input_id, question, post, answer_tag):
        vals = {
            "user_input_id": user_input_id,
            "question_id": question.id,
            "survey_id": question.survey_id.id,
            "skipped": False,
        }
        suil = self.search(
            [
                ("user_input_id", "=", user_input_id),
                ("survey_id", "=", question.survey_id.id),
                ("question_id", "=", question.id),
            ]
        )
        suil.sudo().unlink()

        no_answers = True
        ca_dict = dict_keys_startswith(post, answer_tag + "_")

        comment_answer = ca_dict.pop(("%s_%s" % (answer_tag, "comment")), "").strip()
        if comment_answer:
            vals.update(
                {
                    "answer_type": "text",
                    "value_text": comment_answer,
                }
            )
            self.create(vals)
            no_answers = False

        if question.matrix_subtype == "simple":
            for row in question.labels_ids_2:
                a_tag = "%s_%s" % (answer_tag, row.id)
                if a_tag in ca_dict:
                    no_answers = False
                    vals.update(
                        {
                            "answer_type": "suggestion",
                            "value_suggested": ca_dict[a_tag],
                            "value_suggested_row": row.id,
                        }
                    )
                    self.create(vals)

        elif question.matrix_subtype == "multiple":
            for col in question.labels_ids:
                for row in question.labels_ids_2:
                    a_tag = "%s_%s_%s" % (answer_tag, row.id, col.id)
                    if a_tag in ca_dict:
                        no_answers = False
                        vals.update(
                            {
                                "answer_type": "suggestion",
                                "value_suggested": col.id,
                                "value_suggested_row": row.id,
                            }
                        )
                        self.create(vals)

        elif question.matrix_subtype == "custom":
            for col in question.labels_ids:
                for row in question.labels_ids_2:
                    a_tag = "%s_%s_%s" % (answer_tag, row.id, col.id)
                    if a_tag in ca_dict:
                        no_answers = False
                        if post.get(a_tag):
                            sline = a_tag.split("_")[-1]
                            label_obj = question.labels_ids.browse(int(sline))
                            if label_obj.type == "textbox":
                                vals.update(
                                    {
                                        "answer_type": "text",
                                        "value_suggested": col.id,
                                        "value_suggested_row": row.id,
                                        "value_text": post.get(a_tag),
                                    }
                                )
                            elif label_obj.type == "free_text":
                                vals.update(
                                    {
                                        "answer_type": "free_text",
                                        "value_suggested": col.id,
                                        "value_suggested_row": row.id,
                                        "value_free_text": post.get(a_tag),
                                    }
                                )
                            elif label_obj.type == "numerical_box":
                                vals.update(
                                    {
                                        "answer_type": "number",
                                        "value_suggested": col.id,
                                        "value_suggested_row": row.id,
                                        "value_number": post.get(a_tag),
                                    }
                                )
                            elif label_obj.type == "date":
                                vals.update(
                                    {
                                        "answer_type": "date",
                                        "value_suggested": col.id,
                                        "value_suggested_row": row.id,
                                        "value_date": post.get(a_tag),
                                    }
                                )
                            elif label_obj.type == "dropdown":
                                vals.update(
                                    {
                                        "answer_type": "dropdown",
                                        "value_suggested": col.id,
                                        "value_suggested_row": row.id,
                                        "value_id": int(post.get(a_tag)),
                                    }
                                )
                            else:
                                vals.update(
                                    {
                                        "answer_type": "suggestion",
                                        "value_suggested": col.id,
                                        "value_suggested_row": row.id,
                                    }
                                )
                            self.create(vals)

        if no_answers:
            vals.update(
                {
                    "answer_type": None,
                    "skipped": True,
                }
            )
            self.create(vals)
        return True
