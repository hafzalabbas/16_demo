# -*- coding: utf-8 -*-
# from odoo import http


# class CrmSo(http.Controller):
#     @http.route('/crm_so/crm_so', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_so/crm_so/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_so.listing', {
#             'root': '/crm_so/crm_so',
#             'objects': http.request.env['crm_so.crm_so'].search([]),
#         })

#     @http.route('/crm_so/crm_so/objects/<model("crm_so.crm_so"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_so.object', {
#             'object': obj
#         })
