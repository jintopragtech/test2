# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class ProductWizard(models.TransientModel):

    _name = 'product.wizard'
    _description ='Product Wizard'

    product_ids = fields.Many2many('product.product', string='Products')

    def add_products(self):
        if self._context.get('active_model') == 'sale.order':
            order_line_obj = self.env['sale.order.line']
            for product in self.product_ids:
                order_line = order_line_obj.create({
                    'product_id': product.id,
                    'order_id': self._context.get('active_id', False),
                })
        elif self._context.get('active_model') == 'purchase.order':
            po_line_obj = self.env['purchase.order.line']
            order_id = self.env['purchase.order'].browse(self._context.get('active_id'))
            for product in self.product_ids:
                po_line = po_line_obj.create({
                    'product_id': product.id,
                    'order_id': self._context.get('active_id', False),
                    'name': product.name,
                    'product_qty': 1.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'product_uom': product.uom_id.id,
                    'price_unit': product.lst_price,
                    'display_type': False,
                })
                po_line.onchange_product_id()
        elif self._context.get('active_model') == 'stock.picking':
            picking = self.env['stock.picking'].browse(
                self._context.get('active_id',False))
            location_src_id = picking.location_id.id or picking.picking_type_id.default_location_src_id.id
            location_dest_id = picking.location_dest_id.id or picking.picking_type_id.default_location_src_id.id
            if picking.picking_type_code == 'incoming':
                location_src_id = self.env.ref(
                    'stock.stock_location_suppliers').id
                location_dest_id = self.env.ref(
                    'stock.stock_location_stock').id
            elif picking.picking_type_code == 'outgoing':
                location_src_id = self.env.ref(
                    'stock.stock_location_stock').id
                location_dest_id = self.env.ref(
                    'stock.stock_location_customers').id
            for product in self.product_ids:
                move_line = self.env['stock.move'].create({
                    'product_id': product.id,
                    'picking_id': self._context.get('active_id', False),
                    'name': product.name,
                    'product_uom': product.uom_id.id,
                    'location_id': location_src_id,
                    'location_dest_id': location_dest_id,
                })
                move_line._onchange_product_id()

        elif self._context.get('active_model') == 'account.move':
            invoice_obj = self.env['account.move']
            invoice_line_obj = self.env['account.move.line']
            invoice = invoice_obj.browse(
                self._context.get('active_id', False))
            part = invoice.partner_id
            fpos = invoice.fiscal_position_id
            company = invoice.company_id
            currency = invoice.currency_id
            type = invoice.move_type

            fiscal_position = invoice.fiscal_position_id
            for product in self.product_ids:
                accounts = product.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
                if invoice.is_sale_document(include_receipts=True):
                    # Out invoice.
                    account = accounts['income']
                elif invoice.is_purchase_document(include_receipts=True):
                    # In invoice.
                    account = accounts['expense']
                invoice_line = invoice_line_obj.with_context(check_move_validity=False, skip_account_move_synchronization=True).create({
                    'product_id': product.id,
                    'move_id': self._context.get('active_id', False),
                    'price_unit': product.lst_price,
                    'name': product.name,
                    'quantity': 1.0,
                    'account_id': account.id,
                })
                