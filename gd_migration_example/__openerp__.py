# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Migration example x_date to gn_date',
    'version': '0.9',
    'category': 'Migration',
    'website': 'https://www.odoo.com/',
    'description': """
This is to demonstrate migration features
""",
    'depends': ['base'],
    'data': [
        'views/res_partner.xml',
    ],
    'installable': True,
    'auto_install': False,
}