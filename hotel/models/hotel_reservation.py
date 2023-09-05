import math

from odoo import api, fields, models

from odoo.exceptions import ValidationError

from datetime import datetime


class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _rec_name = 'reservation_seq'

    reservation_seq = fields.Char()
    state = fields.Selection(string="", selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'cancel'), ],
                             default='draft')
    from_date = fields.Date()
    end_date = fields.Date()
    customer = fields.Many2one('res.partner')
    employee = fields.Many2one('hr.employee')
    room = fields.Many2one('hotel.room')
    room_type = fields.Selection(string="", selection=[('single', 'Single'), ('double', 'Double'), ('triple', 'Triple'),
                                                  ('vip', 'VIP'), ],
                            default='single')
    room_cost = fields.Integer(readonly=1)
    total_cost = fields.Integer(readonly=1)
    note = fields.Char()

    # I'm not sure why but sequence generator for reservation_seq doesn't work,
    # although it's the same as the room_seq, I've tried it several times but I can't seem to find the error in it :(
    # @api.model
    # def create(self, vals):
    #     vals['reservation_seq'] = self.env['ir.sequence'].next_by_code("hotel.reservation")
    #     return super(HotelReservation, self).create(vals)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.from_date and record.end_date and record.from_date > record.end_date:
                raise ValidationError("Start date must be before end date!")

    @api.constrains('start_date', 'end_date', 'room')
    def check_other_reservations(self):
        other_reservations = self.env['hotel.reservation'].search([('room', '=', self.room.room_seq)])
        for reservation in other_reservations:
            if reservation == self:
                continue
            if not (self.from_date > reservation.end_date or reservation.from_date > self.end_date):
                raise ValidationError("ROOM IS ALREADY BOOKED!!")

    @api.constrains('room_type')
    def check_cost(self):
        if self.room_type == 'single':
            self.room_cost = 1000
        elif self.room_type == 'double':
            self.room_cost = 2200
        if self.room_type == 'triple':
            self.room_cost = 4100
        if self.room_type == 'vip':
            self.room_cost = 5700

    @api.constrains('start_date', 'end_date')
    def compute_num_days(self):
        delta = self.end_date - self.from_date
        self.total_cost = delta.days * self.room_cost

    def action_change_state_confirm(self):
        # Perform the state change logic here
        for record in self:
            # Update the state field or perform any other necessary operations
            record.write({'state': 'confirm'})

    def action_change_state_cancel(self):
        # Perform the state change logic here
        for record in self:
            # Update the state field or perform any other necessary operations
            record.write({'state': 'cancel'})


