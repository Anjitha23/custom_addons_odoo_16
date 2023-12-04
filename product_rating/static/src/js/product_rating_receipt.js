odoo.define('product_rating.models  ', function(require) {
    'use strict';

    var {Order, Orderline } = require('point_of_sale.models');
    var Registries= require('point_of_sale.Registries');

    const CustomOrder = (Order) => class CustomOrder extends Order{
        export_for_printing(){
            var result = super.export_for_printing(...arguments);
            var product_rating = this.get_product().product_rating;
            result.product_rating = product_rating
            return result;
        }
    }
    Registries.Model.extend(Orderline,CustomOrder);
    });
