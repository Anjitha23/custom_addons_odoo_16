from odoo import http
from odoo.http import request, Controller


class ClearCart(Controller):
    @http.route(['/shop/cart/clear'], type='http', auth="public", website=True)
    def clear_cart(self):
        order = request.website.sale_get_order()
        if order:
            order.order_line.unlink()
            return request.redirect("/shop/cart")
