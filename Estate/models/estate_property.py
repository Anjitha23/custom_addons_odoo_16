from datetime import timedelta

from odoo import fields, models, api


class EstatePlan(models.Model):
    _name = "real.estate.plan"
    _description = "Real Estate Plans"
    # _livingArea = "sequence"

    name = fields.Char('Estate Name',  translate=True, default="NAME")
    description = fields.Text('New Application Real Estate',  translate=True)
    postcode = fields.Char( translate=True)
    property_type = fields.Many2one('property.type', string="Property Type")
    property_tag = fields.Many2many('property.tag', string="Property Tags")
    user_id = fields.Many2one('res.users', string="Buyer")
    partner_id = fields.Many2one('res.partner', string="Seller")
    date_availability = fields.Date(copy=False, default=fields.Datetime.now() + timedelta(days=3 * 30))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer( default="2")
    livingArea = fields.Integer()
    total = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string="Status",
                             selection=[('New', 'new'), ('offer_received', 'Offer_Received'),
                                        ('offer_accepted', 'Offer_Accepted'), ('sold', 'Sold'),
                                        ('canceled', 'Canceled')],  default='New')
    price_id = fields.One2many("property.offer", "property_id")
    # status_id = fields.One2many("property.offer", "property_id")
    total = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area= None
            self.garden_orientation = None


    @api.depends("livingArea", "garden_area")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.livingArea + rec.garden_area

    @api.depends('price_id.price', 'best_price')
    def _compute_best_price(self):
        for rec in self:
            if rec.price_id:
                rec.best_price = max(rec.price_id.mapped("price"))
            else:
                rec.best_price = 0


class EstatePropertyType(models.Model):
    _name = "property.type"
    _description = "property types"

    name = fields.Char()


class EstatePropertyTag(models.Model):
    _name = "property.tag"
    _description = "property tags"
    name = fields.Char()


class EstatePropertyOffers(models.Model):
    _name = "property.offer"
    _description = "property offers"
    price = fields.Float()
    status = fields.Selection(string="Status",
                              selection=[('Accepted', 'accepted'), ('Refused', 'refused')])
    partner_id = fields.Many2one('res.partner', string="Partner")
    property_id = fields.Many2one("real.estate.plan", string="Property Id")


    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_validity")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
