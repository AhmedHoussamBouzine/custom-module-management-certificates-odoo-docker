from odoo import api, fields, models

class DatePresidence(models.TransientModel):
    _name="date.presidence.wizard"
    _description = "date presidence wizard"

    datePresid = fields.Date(string="Date presidence")

