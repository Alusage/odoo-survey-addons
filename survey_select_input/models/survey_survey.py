from odoo import models, fields, api, _


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    tot_selected_survey = fields.Integer(
        "Number of selected surveys", compute="_get_selected_input"
    )

    @api.depends("user_input_ids", "user_input_ids.selected")
    def _get_selected_input(self):
        selected_survey = self.env["survey.user_input"].search(
            [("survey_id", "in", self.ids), ("selected", "=", True)]
        )
        for survey in self:
            survey.tot_selected_survey = len(
                selected_survey.filtered(
                    lambda user_input: user_input.survey_id == survey
                )
            )

    # ACTIONS

    @api.multi
    def action_survey_user_input(self):
        action = super(SurveySurvey, self).action_survey_user_input()
        if self.env.context.get("search_default_selected", False):
            action["display_name"] += _(" selected")
        return action
