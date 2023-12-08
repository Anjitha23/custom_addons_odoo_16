/** @odoo-module **/
import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';
const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
const {useState} = owl;

export class PosComboPopUp extends AbstractAwaitablePopup{
    setup(){
    this.state = useState({
            products: [],
            check_count: [],
            count: 0,
        });
    }
    getPayload() {
            return this.state.check_count;
        }

     ComboClicked(ev,product){
        let occurrence = 0;
        for (const val of this.state.check_count) {
          if (val.category == product.pos_category) {
            occurrence++;
          }
        }
        this.state.count = product.max_count
        const productId = product.product_id;
        const isSelected = this.state.products.includes(productId);
        if(this.state.count <= occurrence || isSelected){
            const productId = product.product_id;
            const isSelected = this.state.products.includes(productId);
            if (isSelected) {
                this.state.products = this.state.products.filter(id => id !== productId);
                this.state.check_count = this.state.check_count.filter(item =>
                item.category !== product.pos_category || item.product !== product.product_name || item.product_id !== product.product_id);
            } else {
                const { confirmed } = this.showPopup('ComboLimit', {
                        title:'Combo alert',
                        body: 'You have already selected maximum item for this category!',
                        confirmText: 'Ok',
                });
            }
        }
        else{
        let val = {}
        val['product_id'] = product.product_id
        val['category'] = product.pos_category
        val['product'] = product.product_name

        const isValExists = this.state.check_count.some(item =>
        item.category === val.category && item.product === val.product && item.product_id === val.product_id
        );

        if (isValExists) {
            this.state.check_count = this.state.check_count.filter(item =>
                item.category !== val.category || item.product !== val.product || item.product_id !== val.product_id
            );
        } else {
            this.state.check_count.push(val);
        }

        const productId = product.product_id;
        const isSelected = this.state.products.includes(productId);
        if (isSelected) {
            this.state.products = this.state.products.filter(id => id !== productId);
        } else {
            this.state.products.push(productId);
        }
        }
    }

    Confirm(ev){
      var order = this.env.pos.get_order();
         for(let val in this.props.data){
              if(this.props.data[val].is_required == true){
                  for(let product in this.props.data[val].products){
                    this.state.products.push(this.props.data[val].products[product].product_id);
                  }
              }
          }
      var combo_product = []
      for(let pro in this.state.products){
        let id = this.state.products[pro]
        const product_details = this.env.pos.db.product_by_id[id]
        let product_value = {}
        product_value['product_id'] = product_details.id
        product_value['category'] = product_details.pos_categ_id[1]
        product_value['product'] = product_details.display_name
        combo_product.push(product_value)
    }
    this.props.this_product.combo_data = combo_product;
    order.add_product(this.props.this_product)
    this.confirm();
    }
    Close(ev){
         this.confirm();
    }
}
PosComboPopUp.template = 'PosComboPopUp';
Registries.Component.add(PosComboPopUp);

