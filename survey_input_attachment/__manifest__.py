# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Survey input attachment",
    "version": "1.0.0",
    "summary": """
        New question type : attachment (img/PDF)
    """,
    "description": """
        This module provides a new type of question in surveys, that allows to join an image or PDF file as answer.
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
        "templates/upload_file.xml",
        "templates/page.xml",
        "templates/survey_print.xml",
        "views/survey_user_input_line.xml",
    ],
    "css": [],
    "images": [],
    "js": [],
    "test": [],
    "demo": [],
    "maintainer": "RemiFr82",
}
