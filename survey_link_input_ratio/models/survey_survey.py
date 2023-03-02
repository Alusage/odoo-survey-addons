from odoo import models, fields, api, _
from odoo.osv.expression import normalize_domain, AND


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    tot_sent_start_survey = fields.Integer(
        "Started sent survey count", compute="_count_sent_input"
    )
    tot_sent_comp_survey = fields.Integer(
        "Completed sent survey count", compute="_count_sent_input"
    )
    sent_start_ratio = fields.Integer(
        string="Started sent survey ratio", compute="_get_sent_start_ratio"
    )
    sent_comp_ratio = fields.Integer(
        string="Completed sent survey ratio", compute="_get_sent_comp_ratio"
    )

    # COMPUTES

    @api.multi
    def _count_sent_input(self):
        UserInput = self.env["survey.user_input"]
        sent_start_survey = UserInput
        if hasattr(UserInput, "date_start") and hasattr(UserInput, "date_done"):
            # Made to be more precise on searching
            # if survey_user_input_dates module  is installed
            # so it also finds one page surveys started
            # which remain to 'new' state until submission
            sent_start_survey = UserInput.search(
                [
                    ("survey_id", "in", self.ids),
                    ("type", "=", "link"),
                    ("date_start", "!=", False),
                    ("date_done", "=", False),
                ]
            )
        else:
            sent_start_survey = UserInput.search(
                [
                    ("survey_id", "in", self.ids),
                    ("type", "=", "link"),
                    ("state", "=", "skip"),
                ]
            )
        sent_comp_survey = UserInput.search(
            [
                ("survey_id", "in", self.ids),
                ("type", "=", "link"),
                ("state", "=", "done"),
            ]
        )
        for survey in self:
            survey.tot_sent_start_survey = len(
                sent_start_survey.filtered(
                    lambda user_input: user_input.survey_id.id == survey.id
                )
            )
            survey.tot_sent_comp_survey = len(
                sent_comp_survey.filtered(
                    lambda user_input: user_input.survey_id.id == survey.id
                )
            )

    @api.depends("tot_sent_start_survey", "tot_sent_survey")
    def _get_sent_start_ratio(self):
        for survey in self:
            if survey.tot_sent_survey == 0:
                survey.sent_start_ratio = 0
            else:
                survey.sent_start_ratio = int(
                    round(
                        100 * (survey.tot_sent_start_survey) / survey.tot_sent_survey, 0
                    )
                )

    @api.depends("tot_sent_comp_survey", "tot_sent_survey")
    def _get_sent_comp_ratio(self):
        for survey in self:
            if survey.tot_sent_survey == 0:
                survey.sent_comp_ratio = 0
            else:
                survey.sent_comp_ratio = int(
                    round(100 * survey.tot_sent_comp_survey / survey.tot_sent_survey, 0)
                )

    # ACTIONS

    @api.multi
    def action_survey_user_input(self):
        ctx = dict(self.env.context)
        search_completed = ctx.get("search_default_completed", None)
        action = super(SurveySurvey, self).action_survey_user_input()
        if ctx.get("link_only", False):
            domain = action.get("domain") or []
            if isinstance(domain, str):
                domain = eval(domain)
            if len(domain) > 1:
                action["domain"] = AND(
                    [[("type", "=", "link")], normalize_domain(domain)]
                )
            else:
                action["domain"] = [("type", "=", "link")]
            action["display_name"] += _(" (from private links)")
        if search_completed is not None:
            act_ctx = action.get("context") or {}
            if isinstance(act_ctx, str):
                act_ctx = eval(act_ctx)
            if "search_default_completed" in act_ctx:
                if bool(act_ctx["search_default_completed"]) is not bool(
                    search_completed
                ):
                    act_ctx["search_default_completed"] = int(bool(search_completed))
                    action["context"] = act_ctx
        return action
