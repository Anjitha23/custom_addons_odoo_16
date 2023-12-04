/**@odoo-module */
import { useService } from "@web/core/utils/hooks";
const { Component, onMounted, useState } = owl;
import { registry } from "@web/core/registry";
const rpc = require('web.rpc');

export class WorkReportDashboard extends Component {
    setup() {
        super.setup(...arguments);
        this.actionReport = useService('action');
        this.dailyWorkReportDashboard = useState({ data: [] });


        onMounted(() => {
            this.loadData();
        });
    }

    loadData() {
        let self = this;

        rpc.query({
            model: 'daily.work.report',
            method: 'get_daily_report_count',
        }).then(function (data) {
            self.dailyWorkReportDashboard.data = data;
        });
    }

    showSubmittedEmployees() {
        // Fetch and display the list of employees who submitted a daily work report
        let submittedEmployees = this.dailyWorkReportDashboard.data.employees_with_email;
        this.actionReport.doAction({
            name: this.env._t('Employees list'),
            type: 'ir.actions.act_window',
            res_model: 'daily.work.report',
            views: [[false, 'tree']],
            view_mode: 'tree',
        });
    }
    showNotSubmittedEmployees() {
        // Fetch and display the list of employees who haven't submitted a daily work report
        let totalEmployees = this.dailyWorkReportDashboard.data.total_employees;
        let submittedEmployees = this.dailyWorkReportDashboard.data.employees_with_email;

        // Ensure totalEmployees and submittedEmployees are numbers
        if (typeof totalEmployees === 'number' && typeof submittedEmployees === 'number') {
            let notSubmittedEmployees = totalEmployees - submittedEmployees;

            if (notSubmittedEmployees > 0) {
                this.actionReport.doAction({
                    name: this.env._t('Employees list'),
                    type: 'ir.actions.act_window',
                    res_model: 'hr.employee',
                    views: [[false, 'tree']],
                    view_mode: 'tree',
                    limit: notSubmittedEmployees,  // Limit the number of displayed records if needed
                });
            } else {
                console.error('Error: No employees found who haven\'t submitted a daily work report');
            }
        } else {
            console.error('Error: Invalid data format for totalEmployees or submittedEmployees');
        }
    }
    showEmployees() {
        // Fetch and display the list of employees who submitted a daily work report
        let submittedEmployees = this.dailyWorkReportDashboard.data.employees_without_email;
        this.actionReport.doAction({
            name: this.env._t('Employees list'),
            type: 'ir.actions.act_window',
            res_model: 'hr.employee',
            views: [[false, 'tree']],
            view_mode: 'tree',
        });
    }
    updateReportData(ev) {
        let dateInput = ev.target;
        if (dateInput) {
            this.dailyWorkReportDashboard.date = dateInput.value;
            this.loadData();
        } else {
            console.error('Error: Date input element not found.');
        }
    }

    getReportData() {
        // Check if a date is selected
        if (!this.dailyWorkReportDashboard.date) {
            alert("Please select a date.");
            return;
        }
        let self = this;
        rpc.query({
            model: 'daily.work.report',
            method: 'get_daily_report_data',
            args: [self.dailyWorkReportDashboard.date],
        }).then(function (data) {
            self.dailyWorkReportDashboard.reports = data;
            // Check if there is no data available
            if (data.length === 0) {
                alert("No data available for the selected date.");
            }
        });
    }
}

WorkReportDashboard.template = 'work_report_dashboard.WorkReportDashboard';
registry.category("actions").add("employee_work_report_dashboard", WorkReportDashboard);

