# -*- coding: utf-8 -*-

from openerp import models, fields, api

class loan(models.Model):
    _name = 'loan.loan'
    _rec_name = 'employee'
    
    state     = fields.Selection([
		('line_manager', 'Line Manager'),
        ('finance_manager', 'Finance Manager'),
        ('coo', 'COO'),
        ('hr_off', 'HR Officer'),
        ],default='line_manager')

    employee = fields.Many2one('hr.employee',string="Employee")
    date        = fields.Date()
    department  = fields.Char()
    description = fields.Text()
    amount      = fields.Integer()
    returned    = fields.Integer()
    net         = fields.Integer()