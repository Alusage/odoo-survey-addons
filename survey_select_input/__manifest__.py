# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Survey answer selection",
    "version": "1.0.0",
    "summary": """
        Mark survey answers as selected
    """,
    "description": """
        This module adds the possibility to select some of the surveys answers in form and list views.
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
        "views/survey_survey.xml",
        "views/survey_user_input.xml",
    ],
    "css": [],
    "images": [],
    "js": [],
    "test": [],
    "demo": [],
    "maintainer": "RemiFr82",
}
