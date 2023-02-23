# -*- coding: utf-8 -*-
{
    'name': "odoo payment by nesrine2",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '15.0',
    'author': "Nesrine Essaies",

    # any module necessary for this one to work correctly
    'depends': ['base','account','payment'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode

}