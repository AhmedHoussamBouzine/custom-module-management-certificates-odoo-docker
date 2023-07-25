from odoo import api, fields, models



class Indice(models.Model):


    _name = "ensaf.indice"
    _description = "ENSAF Enseignant indice"

    grade = fields.Selection([('PES', 'PES'), ('PH', 'PH'), ('PESA', 'PESA')], string="Grade")
    categorie = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], string="Catégorie")
    echelon = fields.Integer(string="Echelon")
    indice = fields.Integer(string="Indice")

