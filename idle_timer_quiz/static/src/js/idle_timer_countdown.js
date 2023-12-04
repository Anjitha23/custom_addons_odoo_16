odoo.define('survey.form.idle_timer', function (require) {
    'use strict';

    // Import required module
    var SurveyForm = require("survey.form");

    // Extend SurveyForm
    SurveyForm.include({
        // Override the start function
        start: function () {
            // Initialize variables for idle time tracking
            this.inactiveTime = 0;
            this.maxInactiveTime = 10;

            var self = this;

            // Call the parent start function and perform additional tasks
            return this._super.apply(this, arguments).then(function () {
                // Get elements and data for idle timer
                self.idle_timer = self.$el.find('.o_survey_timer_idle');
                self.timer = parseInt(self.idle_timer.data('timer'));
                self.is_idle_time = self.idle_timer.data('isidle');

                // If idle time is enabled, initialize and start the idle timer
                if (self.is_idle_time) {
                    self._init_inactiveTimer();
                    $(document).on('mousemove keydown', self.resetInactiveTimer.bind(self));
                }
            });
        },

        // Initialize idle timer
        _init_idle_timer: function () {
            // Increment inactive time
            this.inactiveTime++;

            // If inactive time exceeds the maximum, start the idle timer
            if (this.inactiveTime >= this.maxInactiveTime && !this._isThankYouPage()) {
                clearInterval(this.inactiveInteval);
                this.idle_timer_start = setInterval(this.updateTimer.bind(this), 1000);
            }
        },

        // Check if it's the "Thank You!" page
        _isThankYouPage: function () {
            return $('h1:contains("Thank you!")').length > 0;
        },

        // Update the timer display and submit the form when time is up
        updateTimer: function () {
            // Check if it is not the Thank You page before updating the timer display
            if (!this._isThankYouPage()) {
                var minutes = Math.floor(this.timer / 60);
                var seconds = this.timer % 60;

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                this.idle_timer.text(minutes + ":" + seconds);
            }

            if (this.timer === 0) {
                clearInterval(this.idle_timer_start);
                this._submitForm({
                    'skipValidation': true,
                    'isFinish': true
                });
            } else {
                this.timer--;
            }
        },

        // Reset the inactive timer when user activity is detected
        resetInactiveTimer: function () {
            this.inactiveTime = 0;
            clearInterval(this.idle_timer_start);
            this.idle_timer.text("");
            this.timer = parseInt(this.idle_timer.data('timer'));
            this._pause_inactive_interval();
            this._start_inactive_timer();
        },

        // Initialize the idle timer
        _init_inactiveTimer: function () {
            this._start_inactive_timer();
        },

        // Start the inactive timer interval
        _start_inactive_timer: function () {
            this.inactiveInteval = setInterval(this._init_idle_timer.bind(this), 1000);
        },

        // Pause the inactive timer interval
        _pause_inactive_interval: function () {
            clearInterval(this.inactiveInteval);
        }
    });
});
