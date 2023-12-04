# -*- coding: utf-8 -*-
"""Material Request Table"""
from odoo import api, models, fields, _


class MaterialRequest(models.Model):
    """class for material request model"""
    _name = 'material.request'
    _inherit = 'mail.thread'
    _rec_name = 'material_req'

    material_req = fields.Char(readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    product_ids = fields.One2many('request.product',
                                  'request_id', string='Requested Products')
    date = fields.Date(string='Date', default=lambda self: fields.Date.today())

    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'),
         ('manager_approval', 'Manager Approval'),
         ('head_approval', 'Head Approval'),
         ('approved', 'Approved'), ('rejected', 'Rejected')],
        string='State', default='draft')
    material_request_id = fields.Many2one("purchase.order")
    internal_transfer_id = fields.Many2one("stock.picking")
    po_count = fields.Integer(compute='_compute_po_count', string="Purchase")
    it_count = fields.Integer(compute='_compute_it_count', string="Transfers")
    is_po = fields.Boolean()
    is_it = fields.Boolean()

    def _compute_po_count(self):
        """computes the count of purchase orders"""
        for record in self:
            record.po_count = self.env['purchase.order'].search_count(
                [('material_request_id', '=', self.id)])

    def _compute_it_count(self):
        """computes the count of internal transfers"""
        for record in self:
            record.it_count = self.env['stock.picking'].search_count(
                [('internal_transfer_id', '=', self.id)])

    @api.model
    def create(self, vals):
        """ GENERATING SEQUENCE FOR MATERIAL REQUEST"""
        if vals.get('material_req', _('New')) == _('New'):
            vals['material_req'] = self.env['ir.sequence'].next_by_code(
                'material.request') or _('New')
        return super().create(vals)

    def action_submit(self):
        """action for submit button"""
        self.state = "manager_approval"

    def action_submit_for_approval(self):
        """action for approval button"""
        self.write({'state': "head_approval"})

    def action_head_approve(self):
        """action for approve button"""
        self.write({'state': "approved"})
        # Check if delivery method is 'Purchase Order'
        for record in self.product_ids:
            if record.delivery_method == 'po':
                self.is_po = True
                vendors = record.mapped('product_id.seller_ids')
                for vendor in vendors:
                    rfq_vals = {
                        'partner_id': vendor.partner_id.id,
                        'material_request_id': self.id,
                        'order_line': [fields.Command.create({
                            'product_id': line.product_id.id,
                            'product_qty': line.quantity,
                        }) for line in self.product_ids if
                            vendor in line.product_id.seller_ids]
                    }
                    self.env['purchase.order'].create(rfq_vals)

            elif record.delivery_method == 'it':
                self.is_it = True
                internal_transfer = self.env['stock.picking'].create({
                    "partner_id": self.employee_id.id,
                    'picking_type_id': self.env.ref(
                        'stock.picking_type_internal').id,
                    "origin": self.material_req,
                    "location_id": record.location_id.id,
                    "location_dest_id": record.location_dest_id.id,
                    'internal_transfer_id': self.id,
                })
                internal_transfer.move_ids = [fields.Command.create({
                    'name': record.product_id.name,
                    'product_id': record.product_id.id,
                    "product_uom_qty": record.quantity,
                    'location_id': record.location_id.id,
                    'location_dest_id': record.location_dest_id.id,
                    'picking_id': internal_transfer.id,
                })]

    def action_reject(self):
        """action for reject button"""
        self.write({'state': "rejected"})

    def get_purchase_order(self):
        """function for get the smart button of purchase orders"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('material_request_id', '=', self.id)],
        }

    def get_internal_transfers(self):
        """function for smart button of internal transfers"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfers',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('internal_transfer_id', '=', self.id)],
        }
