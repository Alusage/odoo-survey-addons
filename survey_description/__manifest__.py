# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Survey description",
    "version": "1.0.0",
    "summary": """
        Edit description fields on surveys and pages
    """,
    "description": """
        This module displays standard HTML fields \"Description\" and \"Thank you message\" on survey and survey pages.
    """,
    "author": "RemiFr82",
    "contributors": "Sudokeys",
    "website": "https://remifr82.me",
    "license": "LGPL-3",
    "category": "Marketing",
    # "price": 0,
    # "currency": "EUR",
    "application": False,
    "installable": True,
    "auto_install": False,
    "pre_init_hook": "",
    "post_init_hook": "",
    "uninstall_hook": "",
    "excludes": [],
    "external_dependencies": [],
    "depends": [
        "survey",
    ],
    "data": [
        "views/survey_page.xml",
        "views/survey_survey.xml",
    ],
    "css": [],
    "images": [],
    "js": [],
    "test": [],
    "demo": [],
    "maintainer": "RemiFr82",
}
