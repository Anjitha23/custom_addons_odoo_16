odoo.define('your_module.sale_VariantMixin', function (require) {
    'use strict';

    var VariantMixin = require('sale.VariantMixin');
    var core = require('web.core');
    var _t = core._t;

    VariantMixin.onClickAddCartJSON = function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val()) || 0;
        var quantityChange = $link.has(".fa-minus").length ? -0.1 : 0.1;
        var newQty = parseFloat((previousQty + quantityChange).toFixed(1));

        newQty = Math.min(max, Math.max(min, newQty));

        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    };
});






