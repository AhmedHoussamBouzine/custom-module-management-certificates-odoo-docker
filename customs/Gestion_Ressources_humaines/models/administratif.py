from odoo import api, fields, models


class Administratif(models.Model):
    _name = "ensaf.administratif"
    _description = "ENSAF Administratif"

    som = fields.Integer(string="SOM")
    cin = fields.Char(string="CIN")
    type = fields.Selection([('RH', 'RH'), ('administratif', 'administratif')],
                            string="Type employee")
    nomFr = fields.Char(string="Nom fr")
    prenomFr = fields.Char(string="Prénom fr")
    nomAr = fields.Char(string="Nom Ar")
    prenomAr = fields.Char(string="Prénom Ar")
    sexe = fields.Selection([('masculin', 'Masculin'), ('féminin', 'FEMININ')], string="sexe")
    dateRecru = fields.Date(string="Date de Recrutement")
    dateInst = fields.Date(string="Date d'Installation")
    grade = fields.Selection(
        [('PES', 'PES'), ('PH', 'PH'), ('PESA', 'PESA'), ('Ingenieur Etat 1er grade', 'Ingenieur Etat 1er grade')],
        string="Grade")
    categorie = fields.Selection([('A', 'A'), ('A', 'B'), ('C', 'C')], string="Catégorie")
    dateEffetGr = fields.Date(string="Date d'effet_gr")
    statut = fields.Selection(
        [('Attaché(e)', 'Attaché(e)'), ('Intérimaire', 'Intérimaire'), ('Temporaire', 'Temporaire'),
         ('Titulaire', 'Titulaire'), ('Stagiaire', 'Stagiaire')], string="Statut")
    echelon = fields.Integer(string="Echelon")
    indiceActu = fields.Integer(string="Indice Actuel")
    dateEffetEchel = fields.Date(string="Date d'effet-echel")
    situationPro = fields.Char(string="Situation proposée")
    dateProposition = fields.Date(string="Date proposition")
    diplome = fields.Char(string="Diplôme")
    specialiteDiplome = fields.Char(string="Spécialité (Diplôme)")
    activite = fields.Selection([('enseignement', 'ENSEIGNEMENT'), ('fonctionnaire', 'fonctionnaire')],
                                string="Activite")
    position = fields.Selection([('activite', 'Activite')], string="Position")
    fonction = fields.Char(string="Fonction")
    dateNaissance = fields.Date(string="Date de naissance")
    lieuNaissance = fields.Char(string="Lieu de naissance")
    situationFamiliale = fields.Selection(
        [('Célibataire', 'Célibataire'), ('Marié(e)', 'Marié(e)'), ('Divorcé(e)', 'Divorcé(e)'),
         ('Veuf/Veuve', 'Veuf/Veuve')], string="Situation familiale")
    nbreEnfants = fields.Integer(string="Nombre d'enfants", readonly=True)
    cinFemme = fields.Char(string="CIN de la Femme")
    nomFrFemme = fields.Char(string="Nom fr de la  Femme")
    prenomFrFemme = fields.Char(string="Prénom fr de la Femme")
    nomArFemme = fields.Char(string="Nom Ar de la Femme")
    prenomArFemme = fields.Char(string="Prénom Ar de la Femme")
    adresseFemme = fields.Char(string="Adresse de la Femme")
    sitationProFemme = fields.Char(string="Situation pro de la femme")
    adresse = fields.Char(string="Adresse", readonly=True)
    emailPerso = fields.Char(string="E-mail Personnel")
    emailAcademique = fields.Char(string="E-mail académique")
    tele = fields.Char(string="Tél")
    employee_id = fields.Many2one('ensaf.employee', string='Employee')
