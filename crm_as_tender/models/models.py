# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TenderBoq(models.Model):
    _name = 'tender.boq'
    _description = 'Bill of Quantity'
    _inherit = ['mail.thread']
    _order = "id"
    _check_company_auto = True

    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id

    @api.depends('boq_line_ids.price_total')
    def _total_cost(self):
        """
        Compute the total cost.
        """
        for order in self:
            total_cost = 0.0
            for line in order.boq_line_ids:
                total_cost += line.price_total
            order.update({
                'total_cost': total_cost,
            })

    name = fields.Char(required=1)
    active = fields.Boolean(
        'Active', default=True,
        help="If the active field is set to False, it will allow you to hide the bill of quantity without removing it.")
    cost_updated = fields.Boolean(
        'Updated Cost', default=False,
        help="Please make it true after updating all components cost.")
    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        check_company=True, index=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If a product variant is defined the BOQ is available only for this product.")
    boq_line_ids = fields.One2many('tender.boq.line', 'tender_boq_id', 'BoQ Lines', copy=True)
    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='Unit of Measure', required=True,
        help="This should be the smallest quantity that this product can be produced in.")
    product_uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_product_uom_id, required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control")
    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company)
    total_cost = fields.Monetary(string='Total Cost', store=True, compute='_total_cost')
    user_id = fields.Many2one('res.users', string='User', index=True, default=lambda self: self.env.user)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=["company_id"], store=True,
                                  ondelete="restrict")

    _sql_constraints = [
        ('qty_positive', 'check (product_qty > 0)', 'Product quantity must be positive!'),
    ]


class TenderBoqLine(models.Model):
    _name = 'tender.boq.line'
    _order = "id"
    _rec_name = "product_id"
    _description = 'Bill of Quantity Line'
    _check_company_auto = True

    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id

    product_id = fields.Many2one('product.product', 'Component', required=True, check_company=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product Template', related='product_id.product_tmpl_id',
                                      store=True, index=True)
    company_id = fields.Many2one(
        related='tender_boq_id.company_id', store=True, index=True, readonly=True)
    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='Product Unit of Measure', required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        default=_get_default_product_uom_id,
        required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control",
        domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_cost = fields.Float('Product Cost', required=True, digits='Product Price', default=0.0)
    price_total = fields.Monetary(compute='_compute_amount', string='Total Cost', store=True)
    tender_boq_id = fields.Many2one('tender.boq', 'Tender BoQ', index=True, ondelete='cascade', required=True)
    user_id = fields.Many2one(related='tender_boq_id.user_id', store=True, string='User')
    currency_id = fields.Many2one(related='tender_boq_id.currency_id', depends=['tender_boq_id.currency_id'], store=True,
                                  string='Currency')

    _sql_constraints = [
        ('boq_qty_zero', 'CHECK (product_qty>=0)', 'All product quantities must be greater or equal to 0.!'),
    ]

    @api.depends('product_qty', 'product_cost')
    def _compute_amount(self):
        """
        Compute the amounts of the BOQ line.
        """
        for line in self:
            price = line.product_qty * line.product_cost
            line.update({
                'price_total': price,
            })
