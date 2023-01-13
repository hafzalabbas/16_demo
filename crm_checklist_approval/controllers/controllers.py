# -*- coding: utf-8 -*-
# from odoo import http


# class CrmChecklistApproval(http.Controller):
#     @http.route('/crm_checklist_approval/crm_checklist_approval', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_checklist_approval/crm_checklist_approval/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_checklist_approval.listing', {
#             'root': '/crm_checklist_approval/crm_checklist_approval',
#             'objects': http.request.env['crm_checklist_approval.crm_checklist_approval'].search([]),
#         })

#     @http.route('/crm_checklist_approval/crm_checklist_approval/objects/<model("crm_checklist_approval.crm_checklist_approval"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_checklist_approval.object', {
#             'object': obj
#         })
