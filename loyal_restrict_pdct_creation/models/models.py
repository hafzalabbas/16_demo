# -*- coding: utf-8 -*-

from odoo import api, models, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        res = super(ProductProduct, self).check_access_rights(operation, raise_exception=False)
        if operation == 'create' and self._name == 'product.product' and self.env.user.has_group(
                'loyal_restrict_pdct_creation.group_no_create_edit_product'):
            return False
        return res

    def unlink(self):
        if self.env.user.has_group('loyal_restrict_pdct_creation.group_no_create_edit_product'):
            raise UserError(_('You are not allowed to delete this product. Please contact Administrator.'))
        else:
            return super(ProductProduct, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('loyal_restrict_pdct_creation.group_no_create_edit_product'):
                raise UserError(_('You can not archive/ unarchive this product. Please contact Administrator.'))
            return super(ProductProduct, order).toggle_active()


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        res = super(ProductTemplate, self).check_access_rights(operation, raise_exception=False)
        if operation == 'create' and self._name == 'product.template' and self.env.user.has_group(
                'loyal_restrict_pdct_creation.group_no_create_edit_product'):
            return False
        return res

    def unlink(self):
        if self.env.user.has_group('loyal_restrict_pdct_creation.group_no_create_edit_product'):
            raise UserError(_('You are not allowed to delete this product. Please contact Administrator.'))
        else:
            return super(ProductTemplate, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('loyal_restrict_pdct_creation.group_no_create_edit_product'):
                raise UserError(_('You can not archive/ unarchive this product. Please contact Administrator.'))
            return super(ProductTemplate, order).toggle_active()

