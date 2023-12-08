/** @odoo-module **/

import { Orderline } from 'point_of_sale.models';
import Registries from 'point_of_sale.Registries';

const ComboOrderLine = (Orderline) => class ComboOrderLine extends Orderline{
   export_for_printing(){
        var result = super.export_for_printing();
        result.product = this.get_product();
        return result;

   }
}
Registries.Model.extend(Orderline, ComboOrderLine);
