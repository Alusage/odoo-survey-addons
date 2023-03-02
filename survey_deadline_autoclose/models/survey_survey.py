from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    @api.model
    def cron_close_deadline_survey(self):
        deadline = self.search(
            [
                ("date_deadline", "!=", False),
                ("date_deadline", "<", fields.Date.today()),
            ]
        )
        to_close = deadline.filtered("auto_close")
        if to_close:
            to_close.action_close_survey()
        for survey in deadline - to_close:
            survey.message_post(
                subtype="survey_deadline_autoclose.mail_message_subtype_survey_deadline",
                body=_("This survey has expired."),
            )

    date_deadline = fields.Date(
        string="Deadline", copy=False, track_visibility="onchange"
    )
    auto_close = fields.Boolean(
        string="Auto close",
        default=False,
        help="If checked, the survey will be automatically closed when deadline is overpassed.",
        track_visibility="onchange",
    )

    # ACTIONS

    @api.multi
    def action_send_survey(self):
        self.ensure_one()
        action = super(SurveySurvey, self).action_send_survey()
        action["context"].update(
            {
                "default_date_deadline": self.date_deadline,
            }
        )
        return action

    @api.multi
    def action_close_survey(self):
        stage = self.env["survey.stage"].search([("closed", "=", True)], limit=1)
        if not stage:
            if self.env.context.get("cron", False):
                for survey in self:
                    survey.message_post(
                        subtype="survey_deadline_autoclose.mail_message_subtype_survey_closed",
                        subject=_("Survey closing impossible"),
                        body=_(
                            'Survey should have been automatically closed but no "closed" '
                            "stage was found, the requested operation was impossible to proceed.\n"
                            'To fix this situation, you have to check "Closed" at least on one survey stage.'
                        ),
                    )
            else:
                raise UserError(
                    _(
                        'No "closed" stage found, the requested operation is impossible.\n'
                        'To fix this situation, you have to check "Closed" at least on one survey stage.'
                    )
                )
        else:
            self.write({"stage_id": stage.id})
            for survey in self:
                survey.message_post(
                    subtype="survey_deadline_autoclose.mail_message_subtype_survey_closed",
                    body=_("This survey was automatically closed."),
                )

    # ONCHANGES

    @api.onchange("date_deadline")
    def onchange_date_deadline(self):
        self.ensure_one()
        if not self.date_deadline:
            self.auto_close = False
        elif not self.auto_close:
            self.auto_close = True
