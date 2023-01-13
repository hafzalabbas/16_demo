# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

COST_WARNING = _(u"Please update tender cost for this tender '{}'")
STAGEVALIDATIONERRORMESSAGE = _(u"""Please update document for the tender '{0}'!
You can't move this case forward until you selected all documents on the stage '{1}'. 
 """)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.depends('tender_line_ids.cost_updated')
    def compute_tender_cost_updated(self):
        for lead in self:
            if any(line.cost_updated is False for line in lead.tender_line_ids):
                lead.tender_cost_updated = False
            else:
                lead.tender_cost_updated = True

    @api.depends('check_list_document_ids.document_id')
    def compute_no_of_documents(self):
        for lead in self:
            if any(not line.document_id for line in lead.check_list_document_ids):
                lead.all_documents_updated = False
            else:
                lead.all_documents_updated = True
            if not lead.check_list_document_ids:
                lead.all_documents_updated = True

    @api.depends('stage_id', 'company_id')
    def compute_check_stage(self):
        for lead in self:
            if lead.stage_id.sequence > lead.company_id.checklist_stage_id.sequence:
                lead.check_stage = True
            else:
                lead.check_stage = False

    check_list_document_ids = fields.One2many(
        "check.list.document",
        "lead_id",
        string="Check List Documents",
        copy=False,
    )
    check_stage = fields.Boolean('Stage checking', compute='compute_check_stage')
    tender_cost_updated = fields.Boolean('Total cost updated', compute='compute_tender_cost_updated')
    all_documents_updated = fields.Boolean('All documents updated', compute='compute_no_of_documents')
    waiting_approval_checklist = fields.Boolean('Waiting Approval for Checklist', default=False)
    checklist_approved = fields.Boolean('Checklist Approved', default=False)

    @api.model
    def create(self, vals):
        """
        Overwrite to check whether the checklist is pre-filled and check whether this user might do that

        Methods:
         * _get_initial_stage
        """
        # simulate create with default stage and no checkpoints (so we consider transfer default stage > new stage)
        new_values = {}
        if vals.get("stage_id"):
            default_stage_id = self._get_initial_stage(vals.get("team_id"))
            if default_stage_id and vals.get("stage_id") != default_stage_id.id:
                new_values.update({"stage_id": vals.get("stage_id")})
                vals.update({"stage_id": default_stage_id.id})
        if vals.get("check_list_document_ids"):
            new_values.update({"check_list_document_ids": vals.get("check_list_document_ids")})
            vals.pop("check_list_document_ids")
        task_id = super(CrmLead, self).create(vals)

        # write new stage and checkpoints to trigger checks
        if new_values:
            task_id.write(new_values)
        return task_id

    @api.model
    def _get_initial_stage(self, team_id):
        """
        The method to find default stage based on written team

        Args:
         * team_id - int

        Reutrns:
         * crm.stage object
        """
        if team_id:
            search_domain = ["|", ("team_id", "=", False), ("team_id", "=", team_id)]
        else:
            search_domain = [("team_id", "=", False)]
        search_domain.append(("fold", "=", False))
        return self.env["crm.stage"].search(search_domain, order="sequence", limit=1)

    def write(self, vals):
        if vals.get("stage_id"):
            self._check_checklist_complete(vals)
        return super(CrmLead, self).write(vals)

    def _check_checklist_complete(self, vals):
        if vals.get('company_id'):
            company_id = self.env["res.company"].browse(vals.get("company_id"))
        for lead_id in self:
            if lead_id.tender_cost_updated is False:
                raise ValidationError(COST_WARNING.format(
                    lead_id.name))
            if not vals.get('company_id'):
                company_id = lead_id.company_id
            if lead_id.stage_id == company_id.checklist_stage_id and lead_id.all_documents_updated is False:
                raise ValidationError(STAGEVALIDATIONERRORMESSAGE.format(
                    lead_id.name,
                    lead_id.stage_id.name,))
            if not lead_id.checklist_approved:
                raise AccessError(_("Tender not approved yet."))

    def action_send_for_approval(self):
        for record in self:
            if record.stage_id == record.company_id.checklist_stage_id and record.all_documents_updated is False:
                raise ValidationError(STAGEVALIDATIONERRORMESSAGE.format(
                    record.name,
                    record.stage_id.name))
            record.waiting_approval_checklist = True
            notification_ids = []
            users = self.env['res.users'].search([("groups_id", "=", self.env.ref("crm_checklist.group_crm_approval_user").id)])
            for user in users:
                notification_ids.append((0, 0, {
                    'res_partner_id': user.partner_id.id,
                    'notification_type': 'inbox',
                    # 'notification_status': 'exception'
                }))
            mail_content = _(u"""Please approve this tender '{0}'!
                Users can't move this case forward until you confirm all jobs have been done on the stage '{1}'.
                """).format(
                    record.name,
                    record.stage_id.name,
                )

            record.message_post(body=mail_content,
                           # message_type='email',
                           # message_type='comment',
                           message_type='notification',
                           subtype_xmlid='mail.mt_comment',
                           # partner_ids=self.env.user.partner_id.ids,
                           # )
                           # author_id='self.env.user.partner_id.id',
                           notification_ids=notification_ids)

    def action_approve_checklist(self):
        for record in self:
            record.checklist_approved = True

    @api.onchange('stage_id')
    def update_waiting_approval_checklist(self):
        for record in self:
            if record.stage_id:
                record.waiting_approval_checklist = False
                record.checklist_approved = False
