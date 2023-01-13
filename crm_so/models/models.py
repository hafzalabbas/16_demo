# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Lead(models.Model):
    _inherit = "crm.lead"

    def action_sale_quotations_new(self):
        if self.tender_line_ids:
            if any(line.tender_boq_id.cost_updated is False for line in self.tender_line_ids):
                raise ValidationError(
                    _('Please update cost of tender product components.'))
        return super(Lead, self).action_sale_quotations_new()

    def action_new_quotation(self):
        action = super(Lead, self).action_new_quotation()
        sale_order_lines = [(5, 0, 0)]
        if self.tender_line_ids:
            for line in self.tender_line_ids:
                vals = (0, 0,
                        {
                            'product_id': line.tender_boq_id.product_id.id,
                            'product_uom_qty': line.product_qty,
                            'product_uom': line.product_uom_id.id,
                            'price_unit': line.tender_total_cost/line.tender_product_qty if line.tender_product_qty > 0 else 0,
                            'name': line.tender_boq_id.product_id.get_product_multiline_description_sale()
                         })
                sale_order_lines.append(vals)
            action['context']['default_order_line'] = sale_order_lines
        return action
