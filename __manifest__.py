##############################################################################
#
# Copyright (c) 2023 INVITU - www.invitu.com
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'Event Sale Analytic Report',
    'version': '1.0',
    'author': 'INVITU SARL',
    'website': 'http://www.invitu.com',
    'license': 'AGPL-3',
    'category': 'Marketing/Events',
    'description': '''This module allows analysis between events and sales

    ''',
    'depends': [
        'base',
        'event_sale',
    ],
    'init_xml': [],
    'data': [
        'security/ir.model.access.csv',
        # 'security/account_security.xml',
        'report/event_sale_analytic_report_view.xml',
    ],
    'qweb': [
    ],
    'test': [],
    'demo_xml': [],
    'active': False,
    'installable': True,
}
