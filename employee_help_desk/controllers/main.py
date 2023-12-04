# -*- coding: utf-8 -*-
"""controller file for website"""
from odoo.http import Controller, request, route


class EmployeeTicketMenu(Controller):
    """created a class for Employee Ticket menu"""

    @route(route='/employee-ticket', auth='public', website=True)
    def employee_ticket(self):
        """Check if the logged-in user is an employee or manager"""
        is_employee = (request.env.user.has_group(
            'employee_help_desk.employee_access') and
                       request.env.user.employee_ids)
        is_manager = request.env.user.has_group(
            'employee_help_desk.manager_access')

        """Fetch tickets based on user role"""
        if is_employee:
            tickets = request.env['employee.ticket'].search(
                [('employee_id', '=', request.env.user.employee_ids.id)])
        elif is_manager:
            tickets = request.env['employee.ticket'].search(
                [])  # Allow managers to see all tickets
        else:
            return request.render(
                'employee_help_desk.website_employee_ticket_no_access_template')

        return request.render('employee_help_desk.employee_ticket_template',
                              {'tickets': tickets, 'is_employee': is_employee,
                               'is_manager': is_manager})

    @route('/create/employee-ticket', auth='user', website=True)
    def create_employee_ticket(self, **kw):
        """Check if the logged-in user is an employee"""
        is_employee = request.env.user.has_group(
            'base.group_user') and request.env.user.employee_ids

        if not is_employee:
            return request.render(
                'employee_help_desk.website_employee_ticket_no_access_template')

        ticket_sequence = request.env['ir.sequence'].next_by_code(
            'employee.ticket')
        employee_ticket = request.env['employee.ticket'].create({
            'ticket': ticket_sequence,
            'employee_id': request.env.user.employee_ids.id,
            'date': kw.get('date'),
            'hr_related_requests': kw.get('hr_related_requests'),
            'state': 'submit',
        })

        return request.render(
            'employee_help_desk.website_employee_ticket_success_template',
            {'employee_ticket': employee_ticket})
