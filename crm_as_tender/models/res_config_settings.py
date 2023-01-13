# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    tender_import_stage_id = fields.Many2one('crm.stage', 'Tender Import Stage',
                                             help='Default stage for importing tender lines')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tender_import_stage_id = fields.Many2one('crm.stage', 'Tender Import Stage',
                                             help='Default stage for importing tender lines', readonly=False,
                                             related='company_id.tender_import_stage_id')





