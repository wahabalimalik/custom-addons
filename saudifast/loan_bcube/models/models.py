# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime as dt
from dateutil import relativedelta as rd

# Loan
class Loan(models.Model):
    _name = 'loan.loan'
    _rec_name = 'employee'
    
    state     = fields.Selection([
		('line_manager', 'Line Manager'),
        ('finance_manager', 'Finance Manager'),
        ('coo', 'COO'),
        ('hr_off', 'HR Officer'),
        ],default='line_manager')

    employee    = fields.Many2one('hr.employee',string="Employee")
    job_title   = fields.Char('Job Title')
    department  = fields.Char()
    loan_amount = fields.Integer('Loan Amount')
    request_date= fields.Date('Loan Request Date')
    start_date  = fields.Date('Loan Payment Start Date')
    avg_install = fields.Integer('Installment per Month')
    duration    = fields.Char('Number of Installments')
    returned    = fields.Integer()
    end_date    = fields.Date('Loan Payment End Date')
    remaining   = fields.Integer()
    name = fields.Char(required=True)
    history = fields.One2many('loanhistory.loanhistory','loanhistory_id')


    @api.multi
    def update_history(self):
        self.history.unlink()
        vv =self.env['hr.payslip'].search([('employee_id', '=', self.employee.id),
            ('date_from', '>=', self.start_date),('date_to', '<=', self.end_date)])
        for x in vv:
            if self.start_date <= x.date_from and self.end_date >=x.date_to :
                for v in x.line_ids:
                    if v.salary_rule_id.name == 'loan':
                        loan = v.amount
                        self.history.create({
                            'name' : vv.name,
                            'amount' : loan,
                            'loanhistory_id' : self.id,
                            })
                        break

    @api.onchange('start_date', 'end_date','loan_amount','returned','employee')
    def _onchange_price(self):
        if self.start_date and self.end_date:
            start_date_1  = dt.strptime(self.start_date, "%Y-%m-%d")
            end_date_1   = dt.strptime(self.end_date, "%Y-%m-%d")
            r = rd.relativedelta(end_date_1, start_date_1)
            if r.years > 0:
                years = r.years * 12
                self.duration = years + r.months
                self.avg_install = int(self.loan_amount) / int(self.duration)
            else:
                self.duration = r.months
                self.avg_install = int(self.loan_amount) / int(self.duration)
    	if self.loan_amount:
    		self.remaining = int(self.loan_amount) - int(self.returned)

        if self.employee:
            self.department = self.employee.department_id.name
            self.job_title = self.employee.job_id.name

# Loan History
class LoanHistory(models.Model):
    _name = 'loanhistory.loanhistory'

    name = fields.Char('Payslip Name')
    amount = fields.Integer()

    loanhistory_id = fields.Many2one('loan.loan',ondelete='cascade', required=True)

# HR-Employee
class hr_employee(models.Model):
    _inherit = 'hr.employee'
    @api.model
    def loan_ded(self, payslip):
        duration = 0
        tsheet_obj = self.env['loan.loan']
        timesheets = tsheet_obj.search([('employee', '=', self.id), 
            ('start_date', '<=', payslip.date_from), ('end_date', '>=', payslip.date_to)])
        for tsheet in timesheets:
            duration += tsheet.avg_install
        return duration

# Skip installments request
class LoanSkip(models.Model):
    _name = 'loanskip.loanskip'

    reason = fields.Char('Reason to Skip')
    employee = fields.Many2one('hr.employee',string="Employee")
    date = fields.Date()
    loan = fields.Many2one('loan.loan',string="Loan")