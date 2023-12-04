odoo.define('hospital.dynamic', function (require) {
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var Dynamic = PublicWidget.Widget.extend({
        selector: '.top_doctor_snippets',
        willStart: async function() {
            this._onTopDoctor();
        },
        _onTopDoctor: function () {
            var self = this;
            ajax.jsonRpc('/get_top_doctors', 'call', {})
            .then(function (doctors) {
                var chunks = _.chunk(doctors, 4);
                chunks[0].is_active = true;
                self.$el.find('#courosel').html(
                    qweb.render('hospital.doctor_template', {
                        chunks: chunks
                    })
                );
            });
        }
    });
    PublicWidget.registry.hospital_dynamic = Dynamic;
    return Dynamic;
});
