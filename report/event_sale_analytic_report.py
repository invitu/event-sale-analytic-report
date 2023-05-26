# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EventSaleAnalyticReport(models.Model):
    _name = "event.sale.analytic.report"
    _description = "Event Analytic Statistics"
    _auto = False
    _rec_name = 'event_date'
    _order = 'event_date desc'

    # ==== Event fields ====
    # event_id = fields.Many2one('event.event', readonly=True)
    event_type_id = fields.Many2one('event.type', readonly=True)
    # event_registration_id = fields.Many2one('event.registration', readonly=True)
    seats_used = fields.Integer(string='Number of Participants', readonly=True)
    event_date = fields.Datetime(string='Event Date', readonly=True)

    # company_id = fields.Many2one('res.company', string='Company', readonly=True)
    # company_currency_id = fields.Many2one('res.currency', string='Company Currency', readonly=True)
    # partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)

    # ==== Product fields ====
    product_id = fields.Many2one('product.product', readonly=True)
    categ_id = fields.Many2one('product.category', readonly=True)

    # ==== Sale fields ====
    # sale_order_line_id = fields.Many2one('sale.order.line', readonly=True)

    # ==== Analytic fields ====
    account_id = fields.Many2one('account.analytic.account', readonly=True)
    # account_analytic_line_id = fields.Many2one('account.analytic.line', readonly=True)
    amount = fields.Float('Amount', readonly=True)

    @property
    def _table_query(self):
        return '%s %s %s' % (self._select(), self._from(), self._where())

    @api.model
    def _select(self):
        return '''
            SELECT
            event.id,
            event.date_begin as event_date,
            event.event_type_id,
            event.seats_used,
            move.product_id,
            move.account_id,
            move.amount,
            template.categ_id
        '''

    @api.model
    def _from(self):
        return '''
            FROM event_event event
            LEFT JOIN event_registration registration ON event.id = registration.event_id
            LEFT JOIN sale_order_line sale ON sale.id = registration.sale_order_line_id
            LEFT JOIN sale_order_line_invoice_rel rel ON sale.id = rel.order_line_id
            LEFT JOIN account_move_line account ON account.id = rel.invoice_line_id
            LEFT JOIN account_analytic_line move ON move.move_id = account.id
            LEFT JOIN product_product product ON move.product_id = product.id
            LEFT JOIN product_template template ON product.product_tmpl_id = template.id
            LEFT JOIN product_category category ON template.categ_id = category.id
        '''

    @api.model
    def _where(self):
        return '''
        '''
