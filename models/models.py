# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api,_
from collections import defaultdict
from odoo.exceptions import UserError
from datetime import date, datetime, time

class AccountMove(models.Model):
    _inherit = 'account.move'
    allocated_amount = fields.Monetary(string='allocated_amount')

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    my_method = fields.Boolean(default=False)
    invoice_lines = fields.Many2many("account.move",)
    amount_total = fields.Monetary(string='Amount total' )
    amount_residual = fields.Monetary(string='amount_residual' )

    @api.onchange('partner_id')
    def onchange_invoice_lines(self):
        for rec in self:
            if rec.partner_id:
                invoice_ids = self.env['account.move'].sudo().search(
                    [('partner_id', '=',rec.partner_id.id)])
                rec.sudo().write({"invoice_lines": [(6, 0, invoice_ids.ids)]})

                if invoice_ids.ids != []:
                    rec.my_method=True

    @api.onchange('invoice_lines')
    def onchange_invoice_lines_sum(self):
        for rec in self:
            sum = 0
            sum2 = 0
            sum_allocated_amount = 0
            for inv in rec.invoice_lines:
                sum = sum + inv.amount_total
                sum2 = sum2 + inv.amount_residual
                sum_allocated_amount = sum_allocated_amount + inv.allocated_amount
            rec.sudo().write({"amount_total": sum})
            rec.sudo().write({"amount_residual": sum2})
            rec.sudo().write({"amount": sum_allocated_amount})



    def action_post2(self):
        if self.invoice_lines:

            self.write(
                {'amount': self.amount, 'date': datetime.today(),
                 # 'communication': invoice.name,
                 'partner_type': 'customer',
                 # 'has_invoices': True,
                 # 'invoice_ids': [(6, 0, [int(invoice.id)])]}
                 'reconciled_invoice_ids': [(6, 0, self.invoice_lines.ids)]}
            )
            self.action_post()

