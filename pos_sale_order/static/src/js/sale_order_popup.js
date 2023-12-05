odoo.define('pos_sale_order.SaleOrderPopup', function (require) {
    'use strict';

    const { Popup } = require('point_of_sale.popups');
    const Registries = require('point_of_sale.Registries');

    class SaleOrderPopup extends Popup {
        constructor() {
            super(...arguments);
            this.state = 'draft';
            this.note = '';
        }

        getPayload() {
            return {
                state: this.state,
                note: this.note,
            };
        }
    }

    SaleOrderPopup.template = 'SaleOrderPopup';
    Registries.Component.add(SaleOrderPopup);

    return SaleOrderPopup;
});
