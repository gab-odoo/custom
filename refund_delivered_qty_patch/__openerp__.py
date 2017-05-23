# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Patch Refund Delivered Qty increase',
    'version': '1.0',
    'category': 'Patch',
    'website': 'https://www.odoo.com/',
    'description': """
This is to correct the increase of the delivered qty when refunding SO-Lines containing create task-products
""",
    'depends': ['sale_service'],
    'data': [],
    'installable': True,
    'auto_install': False,
}
