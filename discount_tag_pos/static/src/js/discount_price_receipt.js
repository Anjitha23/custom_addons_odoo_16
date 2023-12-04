odoo.define('discount_tag_pos.models  ', function(require) {
    'use strict';

    var {Order, Orderline } = require('point_of_sale.models');
C
    const DiscountTag = (Order) => class DiscountTag extends Order{
        export_for_printing(){
            var result = super.export_for_printing(...arguments);
            result.discount_price = this.get_product().discount_price
            return result;
        }
    }
    Registries.Model.extend(Orderline,DiscountTag);
});
