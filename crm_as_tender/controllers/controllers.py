# -*- coding: utf-8 -*-
# from odoo import http


# class CrmAsTender(http.Controller):
#     @http.route('/crm_as_tender/crm_as_tender', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_as_tender/crm_as_tender/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_as_tender.listing', {
#             'root': '/crm_as_tender/crm_as_tender',
#             'objects': http.request.env['crm_as_tender.crm_as_tender'].search([]),
#         })

#     @http.route('/crm_as_tender/crm_as_tender/objects/<model("crm_as_tender.crm_as_tender"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_as_tender.object', {
#             'object': obj
#         })
