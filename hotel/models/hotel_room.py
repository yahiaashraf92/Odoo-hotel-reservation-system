from odoo import api, fields, models


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _rec_name = 'room_seq'

    room_seq = fields.Char(readonly=1)
    floor = fields.Integer()
    number = fields.Integer()
    type = fields.Selection(string="", selection=[('single', 'Single'), ('double', 'Double'), ('triple', 'Triple'), ('vip', 'VIP'), ],
                             default='single')
    cost = fields.Integer(readonly=1)

    @api.model
    def create(self, vals):
        vals['room_seq'] = self.env['ir.sequence'].next_by_code("hotel.room")
        return super(HotelRoom, self).create(vals)

    @api.constrains('type')
    def check_cost(self):
        if self.type == 'single':
            self.cost = 1000
        elif self.type == 'double':
            self.cost = 2200
        if self.type == 'triple':
            self.cost = 4100
        if self.type == 'vip':
            self.cost = 5700
