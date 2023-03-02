# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Survey page duplicate",
    "version": "1.0.0",
    "summary": """
        Quick duplicate surveys' pages
    """,
    "description": """
        This module adds a \"Duplicate\" button in pages lines on survey form, only in edit mode.
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
    ],
    "css": [],
    "images": [],
    "js": [],
    "test": [],
    "demo": [],
    "maintainer": "RemiFr82",
}
