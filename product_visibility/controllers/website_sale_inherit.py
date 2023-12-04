# -- coding: utf-8 --
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale, lazy, \
    TableCompute, QueryURL



class WebsiteProductVisibility(WebsiteSale):
    """inherit the website sale controller"""

    @route()
    def shop(self, page=0, category=None, search='', min_price=0.0,
             max_price=0.0, ppg=False, **post):
        result = super(WebsiteProductVisibility, self).shop(page=page, category=category,
                                                  search=search,
                                                  min_price=min_price,
                                                  max_price=max_price, ppg=ppg,
                                                  **post)

        if request.env.user.partner_id.is_allowed_products:
            print(request.env.user.partner_id.is_allowed_products)
            website = request.env['website'].get_current_website()
            if ppg:
                try:
                    ppg = int(ppg)
                    post['ppg'] = ppg
                except ValueError:
                    ppg = False
            if not ppg:
                ppg = website.shop_ppg or 20
            ppr = website.shop_ppr or 4
            pricelist = request.env['product.pricelist'].browse(
                request.session.get('website_sale_current_pl'))

            products = request.env.user.partner_id.is_allowed_products
            partner = request.env.user.partner_id
            if partner.is_allowed_products:
                if partner.allowed_product_ids:
                    products = partner.allowed_product_ids
                    print('product', products)
                elif partner.allowed_category_ids:
                    products = request.env['product.template'].search(
                        [('categ_id', 'child_of', partner.allowed_category_ids.ids)])
            else:
                return result
            keep = QueryURL('/shop', **self._shop_get_query_url_kwargs(
                category and int(category), search, min_price, max_price,
                **post))
            pager = website.pager(url='/shop', total=len(products),
                                  page=page, step=ppg, scope=7, url_args=post)
            offset = pager['offset']
            products = products[offset:offset + ppg]


            products_prices = lazy(
                lambda: products._get_sales_prices(pricelist))
            # setting the values in qcontext
            result.qcontext['bins'] = lazy(
                lambda: TableCompute().process(products, ppg, ppr))
            result.qcontext['get_product_prices'] = lambda product: lazy(
                lambda: products_prices[product.id])
            result.qcontext['ppr'] = ppr
            result.qcontext['ppg'] = ppg
            result.qcontext['pager'] = pager
            result.qcontext['keep'] = keep
            result.qcontext['products'] = products
            result.qcontext['categories'] = False
            result.qcontext['search_product'] = products
            result.qcontext['search_count'] = len(products)
            result.qcontext['products_prices'] = products_prices

        return result