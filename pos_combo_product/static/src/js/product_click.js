/** @odoo-module **/

import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';
const rpc = require('web.rpc')

const PosOrderLine = (ProductScreen) => class PosOrderLine extends ProductScreen{
    async _clickProduct(event) {
        if(event.detail.combo_options_ids[0] != undefined){
                var combo_products = await rpc.query({
                      model: "product.product",
                      method: "get_combo_product",
                      args: [event.detail.combo_options_ids],
                    });
                const { confirmed, payload } = await
                        this.showPopup("PosComboPopUp", {
                          title: this.env._t('POS Combo Products'),
                          this_product: event.detail,
                          data: combo_products,
                      });
                  if (confirmed) {
                    console.log("check_count")
                    }
          }
        else{
            super._clickProduct(event)
        }
    }
}
Registries.Component.extend(ProductScreen, PosOrderLine);
