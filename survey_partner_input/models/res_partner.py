from odoo import models, fields, api, _
from odoo.osv.expression import normalize_domain, AND


class ResPartner(models.Model):
    _inherit = "res.partner"

    tot_sent_survey = fields.Integer("Sent survey count", compute="_count_survey_input")
    tot_comp_survey = fields.Integer(
        "Completed survey count", compute="_count_survey_input"
    )
    tot_sent_comp_survey = fields.Integer(
        "Completed sent survey count", compute="_count_survey_input"
    )
    sent_comp_ratio = fields.Integer(
        string="Completed sent survey ratio", compute="_get_sent_comp_ratio"
    )

    # COMPUTES

    @api.multi
    def _count_survey_input(self):
        UserInput = self.env["survey.user_input"]
        partners_survey = UserInput
        in_onchange = self.env.in_onchange
        origin = in_onchange and self._origin or False
        if in_onchange:
            domain = [
                ("partner_id", "=", self._origin.id),
                "|",
                ("type", "=", "link"),
                ("state", "=", "dones"),
            ]
            if self.email:
                domain = ["|", ("email", "=", self.email)] + domain
            partners_survey = UserInput.search(domain)
        else:
            partners_survey = UserInput.search(
                [
                    "|",
                    ("partner_id", "in", self.ids),
                    ("email", "in", self.filtered("email").mapped("email")),
                    "|",
                    ("type", "=", "link"),
                    ("state", "=", "done"),
                ]
            )
        for partner in self:
            done = partners_survey.filtered(
                lambda sui: (
                    sui.partner_id == (origin or partner)
                    or partner.email
                    and sui.email == partner.email
                )
                and sui.state == "done"
            )
            link = partners_survey.filtered(
                lambda sui: (
                    sui.partner_id == (origin or partner)
                    or partner.email
                    and sui.email == partner.email
                )
                and sui.type == "link"
            )
            partner.tot_sent_survey = len(link)
            partner.tot_comp_survey = len(done)
            partner.tot_sent_comp_survey = len(link & done)

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
        self.ensure_one()
        action = self.env.ref("survey.action_survey_user_input").read()[0]
        action["display_name"] += _(" from {}").format(self.display_name)
        # manage context
        ctx = dict(self.env.context)
        link_only = ctx.pop("link_only", False)
        action["context"] = ctx
        # manage domain
        domain = action.get("domain") or []
        if isinstance(domain, str):
            domain = eval(domain)
        if len(domain) > 1:
            domain = AND(
                [
                    ["|", ("partner_id", "=", self.id), ("email", "ilike", self.email)],
                    normalize_domain(domain),
                ]
            )
        else:
            domain = ["|", ("partner_id", "=", self.id), ("email", "ilike", self.email)]
        if link_only:
            if len(domain) > 1:
                domain = AND([[("type", "=", "link")], normalize_domain(domain)])
            else:
                domain = [("type", "=", "link")]
        action["domain"] = domain
        # return updated action
        return action

    # ONCHANGES

    @api.onchange("email")
    def onchange_email(self):
        self.ensure_one()
        if isinstance(self._origin.id, int):
            self._count_survey_input()
