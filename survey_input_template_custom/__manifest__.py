# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Survey input template custom",
    "version": "1.0.0",
    "summary": """
        Customize survey input elements
    """,
    "description": """
        This module allows to customize the survey start and sumbit buttons' labels, the \"Thank you\" page title and the CSS style of input web templates.
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
        "survey_description",
    ],
    "data": [
        "templates/layout.xml",
        "templates/page.xml",
        "templates/sfinished.xml",
        "templates/survey_init.xml",
        "views/survey_survey.xml",
    ],
    "css": [],
    "images": [],
    "js": [],
    "test": [],
    "demo": [],
    "maintainer": "RemiFr82",
}
