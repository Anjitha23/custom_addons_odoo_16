/** @odoo-module **/
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useInputField } from "@web/views/fields/input_field_hook";
const { Component, useRef } = owl;

export class FloatToInt extends Component {
    input = useRef('floatint');

    updateValue(event) {
        // Convert the float value to the nearest integer using Math.round
        const intValue = Math.round(event.target.value);
        // Update the field value without affecting the database
        this.props.update(event.target.value);
        this.input.el.value = intValue.toString();
    }
}

FloatToInt.template = "FloatToInt";
FloatToInt.props = { ...standardFieldProps, options: { type: Object, optional: true } };
FloatToInt.supportedTypes = ['float'];
FloatToInt.extractProps = ({ attrs }) => ({ options: attrs.options });

registry.category("fields").add("float_int", FloatToInt);
