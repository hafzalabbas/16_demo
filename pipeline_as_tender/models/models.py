# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = "crm.lead"

    name = fields.Char('Tender')


class ActivityReport(models.Model):
    _inherit = "crm.activity.report"

    lead_id = fields.Many2one('crm.lead', "Tender", readonly=True)
