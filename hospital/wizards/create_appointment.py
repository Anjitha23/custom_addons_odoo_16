# -*- coding: utf-8 -*-
"""Create Appointment Wizard"""

from odoo import fields, models


class CreateAppointment(models.TransientModel):
    """Wizard for add doctor in Popup window"""
    _name = "create.appointment"
    _description = "Create Appointment"

    def add_doctor(self):
        """Add data to the excisting module-job position:Doctor"""
        return [
            ('job_id', '=', self.env.ref('hospital.doctor_job_position').id)]

    doctor_id = fields.Many2one('hr.employee', string='Doctor',
                                domain=add_doctor, required="True")
    appointment_id = fields.Many2one('dr.appointment', string='')
    patient_card_id = fields.Many2one('patient.card',
                                      string="Patient card", required=True)

    def action_save(self):
        """action for create appointment when we click on save button"""
        self.ensure_one()
        appointment = self.env['dr.appointment'].create({
            'patient_card_id': self.patient_card_id.id,
            'doctor_id': self.doctor_id.id,
        })
        self.appointment_id = appointment.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'form',
            'res_id': appointment.id,
            'res_model': 'dr.appointment',
        }

    def action_cancel(self):
        """action for create appointment"""
        self.write({'state': "cancel"})
