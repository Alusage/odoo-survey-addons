from odoo import models, fields, api


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    selected = fields.Boolean(string="Selected", default=False)

    @api.multi
    def toggle_selected(self):
        unselect = self.filtered("selected")
        unselect.write({"selected": False})
        (self - unselect).write({"selected": True})
