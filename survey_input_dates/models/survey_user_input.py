from odoo import models, fields, api, _


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    date_start = fields.Datetime(
        string="Start date",
        readonly=True,
        help='This date is set when the user clicks on "Start survey" button for the first time.',
    )
    date_done = fields.Datetime(
        string="Date done",
        readonly=True,
        help='This date is set when the user input is set ton "Done" status.',
    )
    duration = fields.Integer(
        string="Duration",
        compute="_get_duration",
        store=True,
        help="Duration in seconds",
    )
    duration_txt = fields.Char(
        string="Duration",
        compute="_get_duration",
        store=True,
    )

    @api.depends("date_start", "date_done")
    def _get_duration(self):
        for input in self:
            start = input.date_start
            done = input.date_done
            if not start:
                input.duration = 0
                input.duration_txt = _("Not started yet")
            elif not done:
                input.duration = 0
                input.duration_txt = _("Not done yet")
            else:
                input.duration = int((done - start).total_seconds())
                input.duration_txt = self.env["ir.qweb.field.duration"].value_to_html(
                    (done - start).total_seconds(),
                    {"unit": "second", "round": "second"},
                )

    @api.multi
    def write(self, vals):
        if vals.get("state", False) == "done":
            vals.update(
                {
                    "date_done": fields.Datetime.now(),
                }
            )
        return super(SurveyUserInput, self).write(vals)
