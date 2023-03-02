from odoo import models, fields, api


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def next_page(self, user_input, page_id, go_back=False):
        res = super(SurveySurvey, self).next_page(user_input, page_id, go_back)
        if not user_input.date_start and page_id == 0:
            user_input.write({
                'date_start': fields.Datetime.now(),
            })
        return res
