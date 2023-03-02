from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    is_template = fields.Boolean(string="Is a template", default=False, copy=True)

    @api.multi
    def copy_data(self, default=None):
        data = super(SurveySurvey, self).copy_data(default)[0]
        default = dict(default or {})
        if (
            self.is_template
            and default.get("is_template", None) is False
            or not self.is_template
            and default.get("is_template", False)
        ):
            data.update({"title": self.title})
        return [data]

    # ACTIONS

    @api.multi
    def create_survey_from_template(self, default={}):
        self.ensure_one()
        if not self.is_template:
            raise UserError(
                _(
                    'You should use the "Copy" secondary action to duplicate a non-template survey.'
                )
            )
        default.update({"is_template": False})
        new_survey = self.copy(default=default)
        return {
            "type": "ir.actions.act_window",
            "res_model": "survey.survey",
            "view_type": "form",
            "view_mode": "form",
            "target": "current",
            "res_id": new_survey.id,
        }

    @api.multi
    def create_template_from_survey(self, default={}):
        self.ensure_one()
        if self.is_template:
            raise UserError(
                _(
                    'You should use the "Copy" secondary action to duplicate a survey template.'
                )
            )
        default.update({"is_template": True})
        new_survey = self.copy(default=default)
        return {
            "type": "ir.actions.act_window",
            "res_model": "survey.survey",
            "view_type": "form",
            "view_mode": "form",
            "target": "current",
            "res_id": new_survey.id,
        }

    @api.multi
    def action_send_survey(self):
        self.ensure_one()
        if self.is_template:
            raise UserError(
                _(
                    "You cannot send a template survey, create a new survey from this template and you'll be able to share it."
                )
            )
        return super(SurveySurvey, self).action_send_survey()
