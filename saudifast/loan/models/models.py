# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime as dt
from dateutil import relativedelta as rd

class loan(models.Model):
    _name = 'loan.loan'
    _rec_name = 'employee'
    
    state     = fields.Selection([
		('line_manager', 'Line Manager'),
        ('finance_manager', 'Finance Manager'),
        ('coo', 'COO'),
        ('hr_off', 'HR Officer'),
        ],default='line_manager')

    employee    = fields.Many2one('hr.employee',string="Employee")
    start_date  = fields.Date('Start Date')
    end_date    = fields.Date('End Date')
    avg_install = fields.Integer('Installment per Month')
    date        = fields.Date()
    department  = fields.Char()
    description = fields.Text()
    amount      = fields.Integer()
    returned    = fields.Integer()
    remaining   = fields.Integer()

    @api.onchange('start_date', 'end_date','amount','returned')
    def _onchange_price(self):
    	if self.start_date and self.end_date:
	    	start_date_1  = dt.strptime(self.start_date, "%Y-%m-%d")
	    	end_date_1   = dt.strptime(self.end_date, "%Y-%m-%d")
    		r = rd.relativedelta(end_date_1, start_date_1)
    		if r.years > 0 :
    			years = r.years * 12
    			self.avg_install = years + r.months
    		else:
    			self.avg_install = r.months
    		print self.avg_install
    	if self.amount:
    		self.remaining = self.amount - self.returned

