# -*- coding: utf-8 -*-
"""Inheriting the controller"""
from odoo.addons.portal.controllers import portal
from odoo.http import Controller, route, request


class ScheduledActivities(Controller):
    """Class for Scheduled Activities details"""

    @route('/my/activities', auth='user', website=True)
    def get_activities(self):
        """Function to get the Scheduled Activities of types 'Meeting' and 'Call'"""
        user = request.env.user

        # Get the IDs of the activity types 'Meeting' and 'Call'
        meeting_activity_type_id = request.env[
            'mail.activity.type'].sudo().search([('name', '=', 'Meeting')],
                                                limit=1).id
        call_activity_type_id = request.env['mail.activity.type'].sudo().search(
            [('name', '=', 'Call')], limit=1).id

        # Get the activity IDs related to the logged-in user and of types 'Meeting' and 'Call'
        activity_ids = user.activity_ids.filtered(
            lambda activity: activity.activity_type_id.id in [
                meeting_activity_type_id, call_activity_type_id]).ids
        scheduled_activities = request.env['mail.activity'].sudo().search(
            [('id', 'in', activity_ids)])

        # Render the template with the scheduled activities
        return request.render(
            'scheduled_activity_portal.portal_activity_details',
            {'activities': scheduled_activities})

    @route('/my/activity/form/<int:activity_id>', auth='user', website=True)
    def get_activity_form(self, activity_id):
        """Function to get the form view of a specific activity"""
        user = request.env.user

        # Search for the specific activity related to the user
        activity = user.activity_ids.filtered(lambda act: act.id == activity_id)

        # Render the form view template for the specific activity
        return request.render('scheduled_activity_portal.portal_activity_form',
                              {'activity': activity})


class ScheduledActivityCount(portal.CustomerPortal):
    """Class for counters"""

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'activity_count' in counters:
            # Get the logged-in user
            user = request.env.user

            # Get the IDs of the activity types 'Meeting' and 'Call'
            meeting_activity_type_id = request.env[
                'mail.activity.type'].sudo().search([('name', '=', 'Meeting')],
                                                    limit=1).id
            call_activity_type_id = request.env[
                'mail.activity.type'].sudo().search([('name', '=', 'Call')],
                                                    limit=1).id

            # Count only activities related to the user and of types 'Meeting' and 'Call'
            values['activity_count'] = len(user.activity_ids.filtered(
                lambda activity: activity.activity_type_id.id in [
                    meeting_activity_type_id, call_activity_type_id]))

        return values
