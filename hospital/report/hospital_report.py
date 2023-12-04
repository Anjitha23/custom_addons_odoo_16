# -*- coding: utf-8 -*-
"""creating an Abstract model here"""

from odoo import api, models, _


class HospitalReport(models.AbstractModel):
    """class for abstract model"""
    _name = "report.hospital.action_patient_report_template"

    @api.model
    def _get_report_values(self, docids, data=None):
        """function to execute the query"""

        docs = self.env['patient.report.wizard'].browse(docids)
        print(docids)
        print(docs)
        print(data)
        return {
            'doc_ids': docids,
            'doc_model': 'patient.report.wizard',
            'docs': docs,
            'data': data,
        },
