# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route


class PartnerMenu(Controller):
    @route(route='/partner', auth='public', website=True)
    def partner(self):
        print('Hello', request.env.uid)
        country_ids = request.env['res.country'].search([])

        return request.render('session_website.website_partner_template',
                              {'country_ids': country_ids})
    @route('/create/partner', auth='public', website=True )
    def create_partner(self, **kw):
        print("create partner", kw)
        partner_id = request.env['res.partner'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email'),
            'phone': kw.get('phone'),
            'street': kw.get('street'),
            'country_id': kw.get('country')
        })
        partner_ids = request.env['res.partner'].sudo().search([],limit=4,order='create_date desc')
        return request.render('session_website.website_partner_success_template',
                                  {'partner_id': partner_id,'partner_ids': partner_ids})

    @route(['''/view/partner/<model("res.partner"):partner>'''], auth='public', website=True)
    def view_partner(self,partner):
        print('view',partner)
        return request.render('session_website.website_partner_view_template',
                              {'partner': partner})


