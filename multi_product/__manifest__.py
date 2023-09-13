# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Add Multiple Products',
    'version' : '1.0',
    'author':'Craftsync Technologies',
    'category': 'Sales',
    'maintainer': 'Craftsync Technologies',
    'summary': """Enable Multi Product Selection""",
    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'depends' : ['sale_management','stock','purchase','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_wizard.xml',
        'views/invoice.xml',
        'views/picking.xml',
        'views/po.xml',
        'views/so.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'price': 4.99,
    'currency': 'EUR',
}
