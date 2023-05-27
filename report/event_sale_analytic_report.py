# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EventSaleAnalyticReport(models.Model):
    _name = "event.sale.analytic.report"
    _description = "Event Analytic Statistics"
    _auto = False
    _rec_name = 'event_date'
    _order = 'event_date desc'

    # ==== Event fields ====
    event_type_id = fields.Many2one('event.type', readonly=True)
    stage_id = fields.Many2one('event.stage', readonly=True)
    active = fields.Boolean(readonly=True)
    seats_used = fields.Integer(string='Number of Participants', readonly=True)
    event_date = fields.Datetime(string='Event Date', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)

    # ==== Analytic fields ====
    account_id = fields.Many2one('account.analytic.account', readonly=True)
    amount = fields.Float('Amount', readonly=True)

    @property
    def _table_query(self):
        return '%s %s %s %s' % (self._select(), self._from(), self._where(), self._group_by())

    @api.model
    def _select(self):
        return '''
            SELECT
            event.id,
            event.stage_id,
            event.active,
            event.company_id,
            event.date_begin as event_date,
            event.event_type_id,
            event.seats_used,
            aal.account_id,
            sum(aal.amount) as amount
        '''

    @api.model
    def _from(self):
        return '''
            FROM event_event event
            INNER JOIN sale_order_line sale ON sale.event_id = event.id
            INNER JOIN sale_order_line_invoice_rel rel ON sale.id = rel.order_line_id
            INNER JOIN account_move_line aml ON aml.id = rel.invoice_line_id
            INNER JOIN account_analytic_line aal ON aal.move_id = aml.id
        '''

    @api.model
    def _where(self):
        return '''
            WHERE aml.parent_state = 'posted'
        '''

    @api.model
    def _group_by(self):
        return '''
            GROUP BY event.id, aal.account_id
        '''


class EventProductAnalyticReport(models.Model):
    _name = "event.product.analytic.report"
    _description = "Event Product Analytic Statistics"
    _auto = False
    _rec_name = 'event_date'
    _order = 'event_date desc'

    # ==== Event fields ====
    event_type_id = fields.Many2one('event.type', readonly=True)
    stage_id = fields.Many2one('event.stage', readonly=True)
    active = fields.Boolean(readonly=True)
    event_date = fields.Datetime(string='Event Date', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)

    # ==== Product fields ====
    product_id = fields.Many2one('product.product', readonly=True)
    categ_id = fields.Many2one('product.category', readonly=True)

    # ==== Analytic fields ====
    account_id = fields.Many2one('account.analytic.account', readonly=True)
    amount = fields.Float('Amount', readonly=True)

    @property
    def _table_query(self):
        return '%s %s %s %s' % (self._select(), self._from(), self._where(), self._group_by())

    @api.model
    def _select(self):
        return '''
            SELECT
            event.id,
            event.stage_id,
            event.active,
            event.company_id,
            event.date_begin as event_date,
            event.event_type_id,
            aal.account_id,
            sum(aal.amount) as amount,
            aal.product_id,
            template.categ_id
        '''

    @api.model
    def _from(self):
        return '''
            FROM event_event event
            INNER JOIN sale_order_line sale ON sale.event_id = event.id
            INNER JOIN sale_order_line_invoice_rel rel ON sale.id = rel.order_line_id
            INNER JOIN account_move_line aml ON aml.id = rel.invoice_line_id
            INNER JOIN account_analytic_line aal ON aal.move_id = aml.id
            INNER JOIN product_product product ON aal.product_id = product.id
            INNER JOIN product_template template ON product.product_tmpl_id = template.id
            INNER JOIN product_category category ON template.categ_id = category.id
        '''

    @api.model
    def _where(self):
        return '''
            WHERE aml.parent_state = 'posted'
        '''

    @api.model
    def _group_by(self):
        return '''
            GROUP BY event.id, aal.account_id, aal.product_id, template.categ_id
        '''
