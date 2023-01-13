# -*- coding: utf-8 -*-
# from odoo import http


# class PiplineAsTender(http.Controller):
#     @http.route('/pipline_as_tender/pipline_as_tender', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pipline_as_tender/pipline_as_tender/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pipline_as_tender.listing', {
#             'root': '/pipline_as_tender/pipline_as_tender',
#             'objects': http.request.env['pipline_as_tender.pipline_as_tender'].search([]),
#         })

#     @http.route('/pipline_as_tender/pipline_as_tender/objects/<model("pipline_as_tender.pipline_as_tender"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pipline_as_tender.object', {
#             'object': obj
#         })
