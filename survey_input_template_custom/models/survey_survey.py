from odoo import models, fields, api, _


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    @api.model
    def _get_default_style(self):
        return _(
            """/* Background frame (start and thank you) */
// .jumbotron {
//   padding: 2rem 1rem;
//   margin-bottom: 2rem;
//   background-color: #e9ecef;
//   border-radius: 0.3rem;
// }
// @media (min-width: 576px) {
//   .jumbotron {
//     padding: 4rem 2rem;
//   }
// }

/* Titles (survey and pages) */
// h1 {
//   font-size: 2.1875rem;
//   font-family: inherit;
//   font-weight: 500;
//   line-height: 1.2;
//   color: inherit;
//   margin-top: 0;
//   margin-bottom: 0.5rem;
// }
/* Descriptions (survey and pages) */
// p {
//   margin-top: 0;
//   margin-bottom: 1rem;
// }

/* Questions titles */
// h2 {
//   font-size: 1.75rem;
//   font-family: inherit;
//   font-weight: 500;
//   line-height: 1.2;
//   color: inherit;
//   margin-top: 0;
//   margin-bottom: 0.5rem;
// }
/* Responses labels (MCQ) */
// label {
//   margin-bottom: 0.5rem;
// }

/* Buttons (start, navigate and submit) */
// .btn-primary {
//   color: #FFFFFF;
//   background-color: #00A09D;
//   border-color: #00A09D;
// }
// .btn-primary:hover {
//   color: #FFFFFF;
//   background-color: #007a77;
//   border-color: #006d6b;
// }"""
        )

    scss_style = fields.Text(string="SCSS style", default=_get_default_style)
    start_btn_label = fields.Char(
        string="Start button label",
        translate=True,
        track_visibility="onchange",
        help='This label will be used in the survey start button. If empty, the label will be "Start survey".',
    )
    submit_btn_label = fields.Char(
        string="Submit button label",
        translate=True,
        track_visibility="onchange",
        help='This label will be used in the survey submit button. If empty, the label will be "Submit survey".',
    )
    thank_you_title = fields.Char(
        string="Thank you page title",
        translate=True,
        help='This title will be used in the survey "Thank you" page. If empty, the label will be "Thank you !".',
    )
