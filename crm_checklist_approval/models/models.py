# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.depends(
        "stage_id", "stage_id.default_crm_check_list_ids", "check_list_line_ids", "team_id",
        "stage_id.default_crm_check_list_ids.team_ids",
    )
    def compute_checklist_completed(self):
        """
        Compute method for 'check_list_len' & 'checklist_progress'

        Methods:
         * _get_filtered of crm.check.list

        Extra info:
         * we filter 'check_list_line_ids' by active stage to overcome cached checpoints in case of stage change
        """
        for lead_id in self:
            stage_id = lead_id.stage_id
            team_id = lead_id.team_id
            default_crm_check_list_ids = stage_id and \
                                         stage_id.default_crm_check_list_ids._get_filtered(stage_id, team_id) or \
                                         self.env["crm.check.list"]
            check_list_len = len(default_crm_check_list_ids)
            check_list_line_ids = lead_id.check_list_line_ids._get_filtered(stage_id, team_id)
            checklist_progress = check_list_len and (len(check_list_line_ids) / check_list_len) * 100 or 0.0
            if checklist_progress == 100:
                lead_id.checklist_completed = True
            else:
                lead_id.checklist_completed = False
                lead_id.checklist_approved = False
                lead_id.waiting_approval_checklist = False

    checklist_completed = fields.Boolean('Checklist Completed', compute=compute_checklist_completed)
    checklist_approved = fields.Boolean('Checklist Approved', default=False)
    waiting_approval_checklist = fields.Boolean('Waiting Approval for Checklist', default=False)

    def action_send_for_approval(self):
        for record in self:
            record.waiting_approval_checklist = True
            notification_ids = []
            users = self.env['res.users'].search([("groups_id", "=", self.env.ref("crm_checklist.group_crm_checklist_superuser").id)])
            for user in users:
                notification_ids.append((0, 0, {
                    'res_partner_id': user.partner_id.id,
                    'notification_type': 'inbox',
                    # 'notification_status': 'exception'
                }))
            mail_content = _(u"""Please approve the opportunity '{0}'!
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

    def _check_checklist_complete(self, vals, team_id):
        if not self.env.user.has_group("crm_checklist.group_crm_checklist_superuser") and not self.env.su:
            new_stage_id = self.env["crm.stage"].browse(vals.get("stage_id"))
            for lead_id in self:
                res = super(CrmLead, lead_id)._check_checklist_complete(vals, team_id)
                default_crm_check_list_ids = lead_id.stage_id and \
                                             lead_id.stage_id.default_crm_check_list_ids._get_filtered(lead_id.stage_id, lead_id.team_id) or \
                                             self.env["crm.check.list"]
                check_list_len = len(default_crm_check_list_ids)
                if check_list_len != 0 and not lead_id.checklist_approved:
                    raise AccessError(_("Waiting for Approval"))
                else:
                    return res

    def action_approve_checklist(self):
        for record in self:
            record.checklist_approved = True
