odoo.define('hospital.calculate_age', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');


    publicWidget.registry.patientDetails = publicWidget.Widget.extend({
        selector: '.o_patient_details',
        events: {
            'change input[name="dob"]': '_onDateOfBirthChange',
            'change select[id="partner_id"]': '_onPartnerChange',
            'click .btn-primary': '_onCreateButtonClick',

        },
        _onDateOfBirthChange: function() {
            var userDateInput = $('#dob').val();

            if (userDateInput) {
                var birthDate = new Date(userDateInput);
                var today = new Date();

                var age = today.getFullYear() - birthDate.getFullYear();

                if (today.getMonth() < birthDate.getMonth() ||
                    (today.getMonth() === birthDate.getMonth() && today.getDate() < birthDate.getDate())) {
                    age--;
                }
                if (age < 0) {
                    $('.age-error').text('Invalid date of birth. Please check!!');
                    $('#age').val(''); // Clear the age field
                } else {
                    $('.age-error').text(''); // Clear the error message
                    $('#age').val(age);
                }
            }
        },

         _onCreateButtonClick: function (ev) {
            var age = $('#age').val();
            if (age <= 0) {
                ev.preventDefault(); // Prevent form submission
                alert('Invalid date of birth. Please check!');
            }
        },

        _onPartnerChange: function () {
            var self = this;
            var partner_id = $('#partner_id').val();
            if (partner_id) {
                this.$('#partner_name').hide();
                ajax.jsonRpc('/get_partner_details', 'call', {'partner_id': partner_id}).then(function(result) {
                    // Assuming 'result' contains partner details, update the form fields accordingly
                    var partner_details = result;
                    $('#dob').val(partner_details.dob);
                    self._onDateOfBirthChange()
                    $('#gender').val(partner_details.gender);
                });
            }
            else {
                this.$('#partner_name').show();
            }
        },
    });
});
