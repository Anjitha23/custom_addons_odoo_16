# -*- coding: utf-8 -*-
"""inheriting the controller"""
from odoo.addons.portal.controllers import portal
from odoo.http import Controller, route, request


class ManufacturingOrder(Controller):
    """class for manufacturing order details"""

    @route('/my/mo', auth='user', website=True)
    def get_mo(self):
        """function to get the manufacturing orders"""
        mo = request.env['mrp.production'].sudo().search(
            [('customer_id', '=', request.env.user.partner_id.id)])
        return request.render('manufacturing_orders.portal_mo_details',
                              {'orders': mo})


class ManufacturingCount(portal.CustomerPortal):
    """class for counters"""
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'mo_count' in counters:
            values['mo_count'] = request.env[
                'mrp.production'].sudo().search_count(
                [('customer_id', '=', request.env.user.partner_id.id)])
        return values
