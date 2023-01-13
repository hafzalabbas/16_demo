# -*- coding: utf-8 -*-
# from odoo import http


# class CrmChecklist(http.Controller):
#     @http.route('/crm_checklist/crm_checklist', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_checklist/crm_checklist/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_checklist.listing', {
#             'root': '/crm_checklist/crm_checklist',
#             'objects': http.request.env['crm_checklist.crm_checklist'].search([]),
#         })

#     @http.route('/crm_checklist/crm_checklist/objects/<model("crm_checklist.crm_checklist"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_checklist.object', {
#             'object': obj
#         })
