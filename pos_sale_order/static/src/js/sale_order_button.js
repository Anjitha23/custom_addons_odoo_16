odoo.define('point_of_sale.SaleOrderButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

    class SaleOrderButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }

        async onClick() {
            const getOrderline = this.env.pos.get_order().get_selected_orderline();
            const selectedCustomer = this.env.pos.get_order().get_partner();

            if (!selectedCustomer) {
                // Display error popup if no order line or customer is selected
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('Please select a customer before creating a sale order.'),
                });
                return;
            }
            if (!getOrderline){
             // Display error popup if no order line or customer is selected
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('Please select at least one product in order line before creating a sale order.'),
                });
                return;
            }

            const { confirmed, payload: selectedOption } = await this.showPopup('SelectionPopup', {
                title: this.env._t('Create Sale Order'),
                list: [
                    {'id': 'draft', 'label': "Draft", 'item': "draft"},
                    {'id': 'confirm', 'label': "Confirm", 'item': "sale"},
                ]
            });

            if (confirmed) {
                try {
                    const reference = await this.createSaleOrder(selectedOption);
                    if (reference) {
                        console.log('Sale Order Reference:', reference);

                        // Display confirmation popup
                        await this.showPopup('ConfirmPopup', {
                            title: this.env._t('Sale Order Created'),
                            body: this.env._t(`Order Ref: ${reference}`),
                        });
                    } else {
                        console.error('Unable to retrieve Sale Order reference.');
                    }
                } catch (error) {
                    console.error('Error creating Sale Order:', error);
                }
            }
        }

        async createSaleOrder(state) {
            const order = this.env.pos.get_order();

//            // Ensure that a customer is set on the order
//            if (!order.get_partner()) {
//                console.error('Customer is not set on the order.');
//                return;
//            }

            // Customize this based on your Odoo model and fields
            const orderData = {
                partner_id: order.get_partner().id,
                state: state,  // 'draft' or 'sale' (or other valid state)
                // Add other fields as needed
            };

            try {
                const createdSaleOrderID = await this.rpc({
                    model: 'sale.order',
                    method: 'create',
                    args: [orderData],
                });

                // Fetch the created sale order to get the reference
                const createdSaleOrder = await this.rpc({
                    model: 'sale.order',
                    method: 'read',
                    args: [createdSaleOrderID, ['name']],
                });

                if (createdSaleOrder && createdSaleOrder[0] && createdSaleOrder[0].name) {
                    const reference = createdSaleOrder[0].name;

                    // Add order lines to the created sale order
                    for (const line of order.get_orderlines()) {
                        await this.rpc({
                            model: 'sale.order.line',
                            method: 'create',
                            args: [{
                                order_id: createdSaleOrderID,
                                product_id: line.product.id,
                                name: line.product.display_name,
                                product_uom_qty: line.get_quantity(),
                                product_uom: line.product.uom_id[0],
                                price_unit: line.get_unit_price(),
                                // Add other order line fields as needed
                            }],
                        });
                    }

                    // Return the reference of the created sale order
                    return reference;
                } else {
                    console.error('Unable to retrieve Sale Order reference.');
                }
            } catch (error) {
                console.error('Error creating Sale Order:', error);
                throw error;
            }
        }
    }

    SaleOrderButton.template = "SaleOrderButton";
    ProductScreen.addControlButton({
        component: SaleOrderButton,
        position: ['before', "RefundButton"],
    });

    Registries.Component.add(SaleOrderButton);

    return SaleOrderButton;
});
