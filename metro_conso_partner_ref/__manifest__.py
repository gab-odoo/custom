# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Consolidation Partner Reference on Account Move Lines',
    'version': '1.0',
    'category': 'Metro',
    'description': """
Consolidation Partner Reference on Account Move Lines
    """,
    'author': 'Odoo SA',
    'depends': [
        'account_accountant',
    ],
    'data': [
        'data/fields.xml',
        'views/account_move_line.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
