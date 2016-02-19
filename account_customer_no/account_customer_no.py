# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2016 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, models, fields, _
import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit ='res.partner'

    customer_no = fields.Char('Customer Number', compute='_get_customer_no', store=True)

    @api.depends('ref', 'parent_id.ref')
    @api.one
    def _get_customer_no(self):
        if self.parent_id:
            self.customer_no = self.parent_id.customer_no
        else:
            self.customer_no = self.ref

    @api.v7
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=10):
        if context.get('customer_no_search'):
            return self.name_get(cr, uid, self.pool.get('res.partner').search(cr, uid, [('ref', '=ilike', '%s%%' % name)])) + super(res_partner, self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)
        else:
            return super(res_partner, self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    customer_no = fields.Char('Customer/Supplier Number', related="partner_id.customer_no", store=True)

class account_move(models.Model):
    _inherit = 'account.move'

    customer_no = fields.Char('Customer Number', related="partner_id.customer_no", store=True)

class account_move_line(models.Model):
    _inherit = 'account.move.line'

    customer_no = fields.Char('Customer Number', related="partner_id.customer_no", store=True)
