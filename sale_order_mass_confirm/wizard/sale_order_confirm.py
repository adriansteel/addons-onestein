# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError, Warning

class SaleOrderConfirmWizard(models.TransientModel):
    _name = "sale.order.confirm.wizard"
    _description = "Wizard - Sale Order Confirm"

    @api.model
    def default_get(self, fields):
        rec = super(SaleOrderConfirmWizard, self).default_get(fields)
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')

        if active_ids:
            sale_orders = self.env['sale.order'].browse(active_ids)

            if len(sale_orders) == 1:
                raise Warning('Please select more than 1 Quotation')

            if any(quote.state == 'cancel' for quote in sale_orders):
                raise Warning ("Please unselect the cancelled Quotation(s) - (where Status is 'Cancelled')")

            if any(quote.state == ['done','sale'] for quote in sale_orders):
                raise Warning ("Please unselect the Sales Order(s) - (where Status is not 'Quotation')")

            if len(sale_orders) > 80:
                raise Warning('Please select no more than 80 Quotations at a time for the best performance')

        return rec

    @api.multi
    def confirm_sale_orders(self):
        sale_obj = self.env['sale.order']
        orders = sale_obj.browse(self._context.get('active_ids', []))
        for order in orders:
            order.action_confirm()
