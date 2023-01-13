# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class Lead(models.Model):
    _inherit = "crm.lead"

    tender_line_ids = fields.One2many('tender.product.line', 'crm_lead_id', 'Tender Products', copy=False)
    tender_import_stage = fields.Boolean(string='Tender Import Stage', compute='_compute_tender_import_stage', readonly=False, store=True, copy=False)

    @api.depends('company_id', 'stage_id')
    def _compute_tender_import_stage(self):
        for lead in self:
            if lead.company_id.tender_import_stage_id == lead.stage_id:
                lead.tender_import_stage = True
            else:
                lead.tender_import_stage = False


class TenderProductLine(models.Model):
    _name = 'tender.product.line'
    _order = "id"
    _rec_name = "tender_boq_id"
    _description = 'Tender Product Line'
    _check_company_auto = True

    tender_boq_id = fields.Many2one('tender.boq', 'Item Description', required=True, check_company=True)
    cost_updated = fields.Boolean('Updated Cost',
                                  related='tender_boq_id.cost_updated', help="Please make it true after updating all components cost.")
    tender_product_qty = fields.Float('Quantity', related='tender_boq_id.product_qty', digits='Unit of Measure')
    tender_total_cost = fields.Monetary(string='Total Cost', related='tender_boq_id.total_cost')
    company_id = fields.Many2one(
        related='crm_lead_id.company_id', store=True, index=True, readonly=True)
    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='Product Unit of Measure', required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Units',
        required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control",
        domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='tender_boq_id.product_uom_id.category_id')
    estimated_rate = fields.Float('Estimated Rate', required=True, digits='Product Price', default=0.0)
    estimated_total = fields.Monetary('Estimated Total', required=True, digits='Product Price', default=0.0)
    estimated_total_words = fields.Text('Estimated Total in Words')
    total_amount = fields.Monetary(compute='_compute_amount', string='Total Amount', store=True)
    total_amount_words = fields.Text(compute='_compute_amount', string='Total Amount in Words', store=True)
    crm_lead_id = fields.Many2one('crm.lead', 'Tender', index=True, ondelete='cascade', required=True)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True,
                                  string='Currency')
    user_id = fields.Many2one(related='crm_lead_id.user_id', depends=['crm_lead_id.user_id'], store=True,
                                  string='Salesperson')

    _sql_constraints = [
        ('boq_qty_zero', 'CHECK (product_qty>=0)', 'All product quantities must be greater or equal to 0.!'),
    ]

    def english_amt2words(self, amount, currency, change, precision):
        change_amt = (amount - int(amount)) * pow(10, precision)
        words = '{main_word} {main_amt}'.format(
            main_word=currency,
            main_amt=num2words(int(amount)),

        )
        change_amt = int(round(change_amt))
        # words = words.title()
        if change_amt > 0:
            words += ' and {change_word} {change_amt}'.format(
                change_word=change,
                change_amt=num2words(change_amt),

            )
        words += ' Only'
        words = words.title()
        words = words.replace('And', 'and')
        words = words.replace(',', '')
        return words

    @api.depends('tender_product_qty', 'tender_total_cost', 'currency_id', 'product_qty', 'tender_boq_id.boq_line_ids')
    def _compute_amount(self):
        """
        Compute the amounts of the tender product.
        """
        for line in self:
            price = line.product_qty * (line.tender_total_cost/line.tender_product_qty if line.tender_product_qty > 0 else 0)
            amount_words = line.english_amt2words(price, line.currency_id.currency_unit_label, line.currency_id.currency_subunit_label, line.currency_id.decimal_places)
            line.update({
                'total_amount': price,
                'total_amount_words': amount_words
            })
        return
