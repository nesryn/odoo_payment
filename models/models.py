# -*- coding: utf-8 -*-
import base64
import json

from odoo import models, fields, api,_
from collections import defaultdict
from odoo.exceptions import UserError
from datetime import date, datetime, time

class AccountMove(models.Model):
    _inherit = 'account.move'
    allocated_amount = fields.Monetary(string='allocated_amount', readonly=False)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    my_method = fields.Boolean(default=False,)
    invoice_lines = fields.Many2many("account.move")
    amount_total = fields.Monetary(string='Amount total' )
    amount_residual = fields.Monetary(string='amount_residual' )


    @api.onchange('partner_id')
    def onchange_invoice_lines(self):
        for rec in self:
            print(self.id)
            if rec.partner_id:
                invoice_ids = self.env['account.move'].sudo().search(
                    [('partner_id', '=',rec.partner_id.id),('move_type','in',('out_invoice','in_invoice')),('state','=','posted'),('payment_state','in',('not_paid','partial'))])
                rec.sudo().write({"invoice_lines": [(6, 0, invoice_ids.ids)]})
                rec.sudo().write({'reconciled_invoice_ids': [(6, 0, self.invoice_lines.ids)]})




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
            if  rec.invoice_lines:
                rec.my_method = True

    def action_post2(self):
        if self.invoice_lines:
            for rec in self.invoice_lines:
                vals = {'amount': rec.allocated_amount, 'date': datetime.today(),
                     # 'communication': invoice.name,
                     # 'has_invoices': True,
                     # 'invoice_ids': [(6, 0, [int(invoice.id)])]
                }

                if self.payment_type == "inbound":
                    vals['reconciled_invoice_ids']= [(4, rec.id)]
                self.sudo().write(vals)
                for inv in self.invoice_lines:
                    try:

                        inv.payment_id=self.id
                        invoice_id = self.env['account.move'].sudo().search(
                            [('name', '=', inv.invoice_outstanding_credits_debits_widget)])
                        invoice_outstanding_credits_debits_widget2=json.loads(inv.invoice_outstanding_credits_debits_widget)
                        id_cont =invoice_outstanding_credits_debits_widget2['content'][0]['id']
                        inv.js_assign_outstanding_line(id_cont)
                    except Exception as E:
                        pass
            #
            self.action_post()
