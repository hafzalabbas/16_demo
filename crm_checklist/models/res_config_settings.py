# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    checklist_stage_id = fields.Many2one('crm.stage', 'Checklist Stage',
                                             help='Default stage for checking checklist')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    checklist_stage_id = fields.Many2one('crm.stage', 'Checklist Stage',
                                             help='Default stage for checking checklist', readonly=False,
                                             related='company_id.checklist_stage_id')





