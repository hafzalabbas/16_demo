# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError

ACESSERRORMESSAGE = _(u"""Sorry, but you don't have rights to confirm/disapprove '{0}'!
Contact your system administator for assistance.""")


class CrmCheckList(models.Model):
    """
    The model to keep check list items
    """
    _name = "crm.check.list"
    _description = "Check List"

    name = fields.Char(string="Name", required=True)


class CheckListDocument(models.Model):
    """
    The model to keep checklist document
    """
    _name = "check.list.document"
    _description = "Check List Document"

    check_list_id = fields.Many2one("crm.check.list", string="Check Item", required=True)
    lead_id = fields.Many2one("crm.lead", string="Tender", required=True)
    document_id = fields.Many2one('documents.document', 'Document')
    user_id = fields.Many2one("res.users", "User", default=lambda self: self.env.user.id)
