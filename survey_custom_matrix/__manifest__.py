# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Survey Custom Matrix",
    "version": "1.0.0",
    "summary": """
        Customize matrix response fields type
    """,
    "description": """
        This module adds a new type \"Custom\" for matrix questions that allows to ask for answer types different from radio button or checkbox in the matrix grid.
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
        "security/ir_model_access.xml",
        "templates/matrix.xml",
        "reports/user_input.xml",
        "views/survey_question.xml",
        "views/survey_user_input.xml",
        "views/survey_user_input_line.xml",
    ],
    "css": [],
    "images": [],
    "js": [],
    "test": [],
    "demo": [],
    "maintainer": "RemiFr82",
}
