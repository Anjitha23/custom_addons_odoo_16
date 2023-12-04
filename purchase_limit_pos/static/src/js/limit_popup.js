odoo.define('purchase_limit_pos.models', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const MyProductScreen = (ProductScreen) => class MyProductScreen extends ProductScreen {
        async _onClickPay() {
            const order = this.env.pos.get_order();
            const partnerSelected = order.partner;
            const currentPartner = this.currentOrder.get_partner();

            if (!partnerSelected) {
                const { confirmed } = await this.showPopup('ErrorPopup', {
                    title: 'Select a Customer',
                    body: 'Please select a customer to continue with the payment.'
                });

                if (confirmed) {
                    return false; // You can choose to return false here to prevent further processing.
                }
            } else {
                const purchaseLimit = currentPartner.is_purchase_limit || 0;
                const getLimit = currentPartner.add_limit
                const totalAmount = order.get_total_with_tax();

                if (purchaseLimit && totalAmount > purchaseLimit) {
                    const { confirmed } = await this.showPopup('ErrorPopup', {
                        title: 'Purchase Limit Exceeded',
                        body: `The purchase limit for this customer is ${getLimit}. You have exceeded the limit with a total of ${totalAmount}.`
                    });

                    if (!confirmed) {
                        return false; // You can choose to return false here to prevent further processing.
                    }
                }
                else {
                    return super._onClickPay();
                }
            }
        }
    }

    Registries.Component.extend(ProductScreen, MyProductScreen);
});
