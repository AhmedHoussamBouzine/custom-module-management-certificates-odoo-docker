import datetime
from datetime import date
from datetime import datetime
from odoo import api, fields, models


class Document_ensg(models.Model):
    _name = "ensaf.document.enseignant"
    _description = "Ensaf documents enseignant"

    enseignant = fields.Many2one('ensaf.enseignant', string="Enseignant")
    nomAr = fields.Char(string="Nom",related='enseignant.nomAr')
    prenomAr = fields.Char(string="Prenom",related='enseignant.prenomAr')
    nom = fields.Char(string="Nom document")
    documents = fields.Binary(string="Documents")
