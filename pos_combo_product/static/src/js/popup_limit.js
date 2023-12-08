/** @odoo-module **/
import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';
const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
const {useState} = owl;

export class ComboLimit extends AbstractAwaitablePopup{

}
ComboLimit.template = 'LimitPopUp';
Registries.Component.add(ComboLimit);

