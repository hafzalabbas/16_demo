# -*- coding: utf-8 -*-
# from odoo import http


# class LoyalRestrictPdctCreation(http.Controller):
#     @http.route('/loyal_restrict_pdct_creation/loyal_restrict_pdct_creation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/loyal_restrict_pdct_creation/loyal_restrict_pdct_creation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('loyal_restrict_pdct_creation.listing', {
#             'root': '/loyal_restrict_pdct_creation/loyal_restrict_pdct_creation',
#             'objects': http.request.env['loyal_restrict_pdct_creation.loyal_restrict_pdct_creation'].search([]),
#         })

#     @http.route('/loyal_restrict_pdct_creation/loyal_restrict_pdct_creation/objects/<model("loyal_restrict_pdct_creation.loyal_restrict_pdct_creation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('loyal_restrict_pdct_creation.object', {
#             'object': obj
#         })
