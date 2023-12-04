# -*- coding: utf-8 -*-
"""Report form Wizard"""
import datetime
import io

import xlsxwriter

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import date_utils
from odoo.tools.safe_eval import json
from datetime import datetime



class PatientReport(models.TransientModel):
    """Wizard for generate report in Popup window"""
    _name = "patient.report.wizard"
    _description = "Patient Report Wizard"

    partner_id = fields.Many2one("patient.card",
                                 string='Patient Name')

    def add_doctor(self):
        """Add data to the existing module-job position:Doctor"""
        return [
            ('job_id', '=', self.env.ref('hospital.doctor_job_position').id)]

    doctor_id = fields.Many2one('hr.employee', string='Doctor',
                                domain=add_doctor)
    department_id = fields.Many2one('hr.department', string="Department")

    from_date = fields.Date(string='From', default="")
    to_date = fields.Date(string='To', default="")
    disease_id = fields.Many2one("disease", string="Diseases")

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        """Adding validation error for dates"""
        if self.to_date and self.from_date:
            for record in self:
                if record.from_date > record.to_date:
                    raise models.ValidationError(
                        'To date must be after from date!')

    def generate_report(self):
        """Query to filter the records"""
        query = """
                 SELECT 
                     ROW_NUMBER() OVER () as serial_no,
                     pc.patient as op,
                     res_partner.name as partner,
                     c.date,
                     e.name as doctor,
                     dpt.name as department,
                     d.name as disease
                 FROM 
                     consultation c
                 INNER JOIN 
                     patient_op po ON c.patient_card_id = po.id
                 INNER JOIN 
                     patient_card pc ON po.patient_card_id = pc.id
                 INNER JOIN 
                     res_partner ON pc.partner_id = res_partner.id
                 INNER JOIN 
                     hr_employee e ON po.doctor_id = e.id
                 INNER JOIN 
                     hr_department dpt ON e.department_id = dpt.id
                 INNER JOIN 
                     disease d ON c.disease = d.id"""
        # print(query)

        if self.partner_id:
            query += """ WHERE pc.id = '%s'""" % self.partner_id.id
        if self.doctor_id:
            query += """ AND po.doctor_id = '%s'""" % self.doctor_id.id
        if self.from_date and self.to_date:
            query += f" AND c.date <= '{self.to_date}'"

        if self.disease_id:
            query += """ AND c.disease = '%s'""" % self.disease_id.id

        if self.department_id:
            query += """ AND e.department_id = '%s'""" % self.department_id.id
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        # print(result)
        if not result:
            raise UserError(_("No matching records to generate reports."))
        print('result')
        return result

    def action_print_report(self):
        """function for generate report button"""
        # print("11111")
        pdf = self.generate_report()
        # print('pdf1',pdf)
        data = {
            'form_data': self.read()[0], 'pdf': pdf
        }
        print('data', data)
        return (self.env.ref('hospital.action_patient_report_form').
                report_action(self, data=data))

    def print_xls_report(self):
        """function for generate xlsx report button"""
        xlsx = self.generate_report()
        # print('xlsx1',xlsx)
        form_data = self.read()[0]
        validation = self._check_dates()
        data = {
            'form_data': form_data, 'xlsx': xlsx, 'validation': validation
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'patient.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, form_data, response):
        """function to generate xlsx sheet"""
        data = form_data.get('xlsx')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        # Define cell formats
        cell_format = workbook.add_format({'font_size': 12, 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 20})
        sub_head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 16})
        txt = workbook.add_format({'font_size': 10, 'align': 'left'})


        # Write report heading and sub-heading
        sheet.merge_range('E2:G3', 'Medical Report', head)
        default_company = self.env.company

        # Write default company in the report
        sheet.write('B2:C3', 'Company:', cell_format)
        sheet.merge_range('C2:D2', default_company.name, txt)

        creation_date = fields.Datetime.now()  # Get the current date and time
        creation_date = datetime.strftime(creation_date,
                                          '%Y-%m-%d')
        sheet.write('B3', 'Created on:', cell_format)
        sheet.write('C3', creation_date, txt)
        if form_data.get('form_data').get('partner_id'):
            partner_id = form_data.get('form_data').get('partner_id')[0]
            partner_record = self.env['patient.card'].browse(partner_id)
            sub_heading = (f'{partner_record.patient_id}-'
                           f' {partner_record.partner_id.name}')
            sheet.merge_range('E4:G5', sub_heading, sub_head)
        if form_data.get('form_data').get('doctor_id'):
            doctor_id = form_data.get('form_data').get('doctor_id')[0]
            doctor_record = self.env['hr.employee'].browse(doctor_id)
            # Write Doctor's name
            sheet.merge_range('F6:F7', doctor_record.name, sub_head)
            # Write From date and To date
            sheet.write('B9:B10', 'From Date:', cell_format)
        if form_data.get('form_data').get('from_date'):
            from_date = form_data.get('form_data').get('from_date')
            sheet.merge_range('C9:D9', from_date, txt)
            sheet.write('E9', 'To Date:', cell_format)
        if form_data.get('form_data').get('to_date'):
            to_date = form_data.get('form_data').get('to_date')
            sheet.merge_range('F9:G9', to_date, txt)
        # Write table headers
        headers = ['SL no', 'OP', 'Patient name', 'Date', 'Doctor',
                   'Department', 'Disease']
        for col, header in enumerate(headers):
            sheet.write(10, col, header, cell_format)
        for index, item in enumerate(data, start=12):
            sheet.write(index, 0, index - 11, txt)
            sheet.write(index, 1, item['op'], txt)
            sheet.write(index, 2, item['partner'], txt)
            sheet.write(index, 3, item['date'], txt)
            sheet.write(index, 4, item['doctor'], txt)
            sheet.write(index, 5, item['department'], txt)
            sheet.write(index, 6, item['disease'], txt)
            # Adjust column widths
            sheet.set_column('B:B', 10)
            sheet.set_column('C:C', 15)
            sheet.set_column('D:D', 20)
            sheet.set_column('E:E', 15)
            sheet.set_column('F:F', 25)
            sheet.set_column('G:G', 25)
            sheet.set_column('H:H', 25)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
