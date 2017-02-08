# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime as dt
from dateutil import relativedelta as rd

# Fleet
class Fleet(models.Model):
    _inherit = 'account.invoice'

    challan_no  = fields.Char()
    truck_no = fields.Char()
    bilty_no = fields.Char()
    bc_from = fields.Many2one('location.location',string='From')
    to = fields.Many2one('location.location',string='To')
    shipper_invoice_no = fields.Many2one ('purchase.order')
    region = fields.Many2one('region.region')
    quantity = fields.Char()
    weight = fields.Char()
    distance = fields.Char()
    plan = fields.Char('Plan No/Date')
    sale_price = fields.Integer(string="Sale Price : ")
    purchase_price = fields.Integer('Purchase Price')
    profit = fields.Integer()
    supplier = fields.Many2one ('res.partner')

    @api.multi
    def advance_btn(self):
        vv =self.env['account.invoice']
        order_line_data = [
        (0, 0,
            {
                'product_id': 69,
                'product_uom':1,
                'name' : 'Vahicle',
                'product_qty':1,
                'price_unit':self.purchase_price,
                # 'date_planned': self.date_invoice,
            }
        )
        ]
        res = {
        'partner_id' : self.supplier.id,
        'order_line' : order_line_data,
        }
        vv.create(res)
        # self.shipper_invoice_no = hy
        # self.profit = self.sale_price - self.purchase_price

# Location
class Location(models.Model):
    _name = 'location.location'
    name = fields.Char()

# Region
class Region(models.Model):
    _name = 'region.region'
    name = fields.Char()