# -*- coding: utf-8 -*-
"""controller file for website"""
from datetime import datetime
from odoo.http import Controller, request, route


class AppointmentMenu(Controller):
    """created a class for Appointment menu"""

    @route(route='/appointment', auth='public', website=True)
    def appointment(self):
        """form view for doctor appointment model"""
        print('hii')
        patient_card_ids = request.env['patient.card'].sudo().search([])
        doctor_ids = request.env.ref('hospital.doctor_job_position')
        doctor = request.env['hr.employee'].sudo().search(
            [('job_id', '=', doctor_ids.id)])
        return request.render('hospital.book_appointment_template',
                              {'patient_card_ids': patient_card_ids,
                               'doctor_ids': doctor})

    @route(route='/create/appointment', auth='public', website=True)
    def create_appointment(self, **kw):
        """function to create appointment in backend"""
        new_appointment = request.env['dr.appointment'].sudo().create({
            'patient_card_id': kw.get('patient_card_id'),
            'doctor_id': kw.get('doctor_id')
        })

        return request.render(
            'hospital.website_appointment_success_template',
            {'new_appointment': new_appointment})

    @route(route='/patient', auth='public', website=True)
    def patient_card(self):
        """form view for patient card model"""
        partners = request.env['res.partner'].sudo().search([])
        return request.render('hospital.patient_card_template',
                              {'partners': partners})

    @route(route='/create/patient_card', auth='public', website=True)
    def create_patient_card(self, **kw):
        """create patient card through website"""
        partner_id = kw.get('partner_id')
        partner_name = kw.get('new_partner_name')
        partner_gender = kw.get('gender')
        partner_dob = kw.get('dob')
        if partner_dob:
            partner_dob = datetime.strptime(partner_dob, '%Y-%m-%d')
        else:
            partner_dob = False

        if partner_id:
            partner = request.env['res.partner'].sudo().browse(int(partner_id))
            partner_name = partner.name
            partner_gender = partner.gender
            partner_dob = partner.dob

        else:
            partner = request.env['res.partner'].sudo().create({
                'name': partner_name,
                'gender': partner_gender,
                'dob': partner_dob
            })

        new_patient_card = request.env['patient.card'].sudo().create({
            'partner_id': partner.id if partner else None,
            'name': partner_name,
            'gender': partner_gender if partner else kw.get('gender'),
            'age': kw.get('age'),
            'dob': partner_dob if partner else kw.get('dob'),
            'blood_group': kw.get('blood_group')
        })

        return request.redirect(
            '/appointment?patient_card_id=%s' % new_patient_card.id)

    @route('/get_partner_details', type='json', auth='public',website=True)
    def get_partner_details(self, **kw):
        """To fetch the patient details"""
        partner_id = int(kw.get('partner_id'))
        partner = request.env['res.partner'].sudo().browse(partner_id)

        return {
            'name': partner.name,
            'gender': partner.gender,
            'dob': partner.dob,
        }

    @route('/get_top_doctors', type='json', auth='public', website=True)
    def get_top_doctors(self):
        """function to get the employees who have the job title doctor"""
        employees = request.env['hr.employee']
        top_doctors = employees.sudo().search([('is_doctor', '=', True)])
        doctor_data = [{'id': doctor.id, 'name': doctor.name,
                        'image_1920': doctor.image_1920}
                       for doctor in top_doctors]
        return doctor_data

    @route(['''/view/doctor/<model("hr.employee"):doctor>'''], auth='public',
           website=True)
    def view_doctor(self, doctor):
        """function to view the details of the doctor"""
        return request.render('hospital.view_doctor_template',
                              {'doctor': doctor})
