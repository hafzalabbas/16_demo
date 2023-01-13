
from odoo import api,fields,models,_
import xlrd
from xlrd import open_workbook
import tempfile
import binascii
import base64
from odoo.exceptions import ValidationError,UserError
from io import StringIO,BytesIO


class TenderLineExcelImport(models.TransientModel):
    _name = 'tender.line.excel.import'
    _description = 'Tender Line Excel Import'

    name = fields.Binary(string="Choose the file(.xls)", required=True)
    file_name = fields.Char(string="File name")
    crm_lead_id = fields.Many2one('crm.lead', string='Tender')

    def action_import(self):
        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.name))
            fp.seek(0)
            wb = xlrd.open_workbook(filename=fp.name)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        sheet = wb.sheet_by_index(0)
        tender_line_vals = []
        for row in range(sheet.nrows):
            if row >= 1:
                row_vals = sheet.row_values(row)
                boq_id = self.env['tender.boq'].search([('id', '=', int(row_vals[7]))]) if row_vals[7] else False
                uom_id = self.env['uom.uom'].search([('name', 'ilike', row_vals[3])], limit=1)
                if not uom_id:
                    raise UserError(_("Please make sure all the UoM's are created before importing file"))
                if not boq_id:
                    product_vals = {
                        'name': row_vals[1],
                        'detailed_type': 'product',
                        'uom_id': uom_id.id,
                        'uom_po_id': uom_id.id
                    }
                    product = self.env['product.product'].create(product_vals)
                    vals = {
                        'name': row_vals[1],
                        'product_uom_id': uom_id.id,
                        'product_id': product.id,
                    }
                    boq_id = self.env['tender.boq'].create(vals)
                tender_line_vals.append((0, 0, {
                    'tender_boq_id': boq_id.id,
                    'estimated_total': int(row_vals[5]),
                    'estimated_total_words': row_vals[6],
                    'product_qty': int(row_vals[2]),
                    'product_uom_id': uom_id.id,
                    'estimated_rate': int(row_vals[4])
                }))
        self.crm_lead_id.update({'tender_line_ids': tender_line_vals})
        # write = self.crm_lead_id.update({'tender_line_ids': tender_line_vals})
        # if write:
        #     view = self.env.ref('loyal_popup_message.message_wizard')
        #     view_id = view and view.id or False
        #     context = dict(self._context or {})
        #     context['message'] = "Tender lines imported successfully"
        #     return {
        #         'name': 'Success',
        #         'type': 'ir.actions.act_window',
        #         'view_type': 'form',
        #         'view_mode': 'form',
        #         'res_model': 'message.wizard',
        #         'views': [(view_id, 'form')],
        #         'view_id': view_id,
        #         'target': 'new',
        #         'context': context,
        #     }

