import datetime
from datetime import date
from datetime import datetime
from odoo import api, fields, models


class Enseignant(models.Model):
    _name = "ensaf.enseignant"
    _description = "ENSAF Enseignant"
    _inherit = "mail.thread"

    som = fields.Integer(string="SOM", readonly=True)
    originPost = fields.Selection([('création', 'Création'), ('fonctionnaire', 'Fonctionnaire')],
                                  string="Origine de poste")
    type = fields.Selection([('enseignant', 'enseignant')],
                            string="Type employee")
    specialitePost = fields.Char(string="Spécialité du poste", readonly=True)
    cin = fields.Char(string="CIN", readonly=True)
    nomFr = fields.Char(string="Nom fr", readonly=True)
    prenomFr = fields.Char(string="Prénom fr", readonly=True)
    nomAr = fields.Char(string="Nom Ar", readonly=True)
    prenomAr = fields.Char(string="Prénom Ar", readonly=True)
    sexe = fields.Selection([('masculin', 'Masculin'), ('féminin', 'FEMININ')], string="sexe")
    dateRecru = fields.Date(string="Date de Recrutement", readonly=True)
    dateInst = fields.Date(string="Date d'Installation", readonly=True)
    grade = fields.Selection([('PES', 'PES'), ('PH', 'PH'), ('PESA', 'PESA')], string="Grade", readonly=True)
    datePA = fields.Date(string="Date d'effet PA", readonly=True)
    datePH = fields.Date(string="Date d'effet PH", readonly=True)
    datePES = fields.Date(string="Date d'effet PES", readonly=True)
    categorie = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], string="Catégorie", readonly=True)
    dateEffetGr = fields.Date(string="Date d'effet_cate", readonly=True)
    echelon = fields.Integer(string="Echelon", readonly=True)
    dateEffetEchel = fields.Date(string="Date d'effet-echel", readonly=True)
    indiceActu = fields.Integer(string="Indice Actuel", readonly=True)
    situationPro = fields.Char(string="Situation proposée", readonly=True)
    dateProposition = fields.Date(string="Date proposition", readonly=True)
    diplome = fields.Char(string="Diplôme", readonly=True)
    specialiteDiplome = fields.Char(string="Spécialité (Diplôme)", readonly=True)
    departement = fields.Char(string="Département", readonly=True)
    activite = fields.Char(string="Activité")
    position = fields.Char(string="Position")
    fonction = fields.Char(string="Fonction", readonly=True)
    dateNaissance = fields.Date(string="Date de naissance", readonly=True)
    lieuNaissance = fields.Char(string="Lieu de naissance", readonly=True)
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
    statut = fields.Selection(
        [('Attaché(e)', 'Attaché(e)'), ('Intérimaire', 'Intérimaire'), ('Temporaire', 'Temporaire'),
         ('Titulaire', 'Titulaire'), ('Stagiaire', 'Stagiaire')], string="Statut")
    emailPerso = fields.Char(string="E-mail Personnel", readonly=True)
    emailAcademique = fields.Char(string="E-mail académique", readonly=True)
    tele = fields.Char(string="Tél", readonly=True)
    proposition_echlon = fields.Boolean(default=False, readonly=True)
    proposition_categorie = fields.Boolean(default=False, readonly=True)
    proposition_grade = fields.Boolean(default=False, readonly=True)
    proposition_titulaire = fields.Boolean(default=False, readonly=True)
    system = fields.Char(string="Système de promotion", readonly=True)
    attachment_ids = fields.Many2many('ir.attachment', string='attachment', readonly=True)
    state = fields.Selection([('proposer', 'Proposer'), ('valider', 'Valider')], string="Status")
    dateDeligib = fields.Date(string="Date d'éligibilité")
    employee_id = fields.Many2one('ensaf.employee', string='Employee')

    # today = date.today()

    def delete_repition(self, table):
        seen_values = set()
        new_table = []
        for obj in table:
            if getattr(obj, "system") not in seen_values:
                seen_values.add(getattr(obj, "system"))
                new_table.append(obj)
        return new_table

    def get_system_arabe(self, system):
        if system == "rapide":
            return "السريع"
        elif system == "exceptionnel":
            return "الاستثنائي"
        else:
            return "العادي"

    def change_year(self, X):
        date_string = X.strftime('%d-%m-%Y')
        date = datetime.strptime(date_string, '%d-%m-%Y')  # Convert string to datetime object
        previous_year = date.replace(year=date.today().year - 1)  # Subtract 1 from the year
        previous_year_string = previous_year.strftime('%d-%m-%Y')  # Convert datetime object to string
        return previous_year_string  # Output: 2021-04-05

    def search_exceptionnel_records(self, grad, categorie, system):
        related_model = self.env['ensaf.enseignant']
        domain = []
        domain += [('grade', '=', grad)]
        domain += [('categorie', '=', categorie)]
        domain += [('proposition_categorie', '=', True)]
        domain += [('system', 'ilike', system)]
        related_records = related_model.search(domain)
        print(related_records)
        return related_records

    def search_categoriePromo_records(self, grad, categorie):
        if (grad == "PESA"):
            if (categorie == "A"):
                return "B"
            elif (categorie == "B"):
                return "C"
            else:
                return "D"
        else:
            if (categorie == "A"):
                return "B"
            elif (categorie == "B"):
                return "C"

    def get_echlon_indice(self, ech, cat, gra):
        query = """select "indice"  from ensaf_indice WHERE grade='%s' AND categorie='%s' AND echelon=%s""" % (
            gra, cat, int(ech + 1))
        self.env.cr.execute(query)
        indice = self.env.cr.fetchall()

        if (indice != []):
            return indice[0][0]
        else:
            return False

    def get_echlon(self, ech, cat, gra):
        if (self.get_echlon_indice(ech, cat, gra) != False):
            return ech + 1
        else:
            return ech

    def get_dat_affictation_ech(self, dat):
        if (dat == False):
            return "تاريخ التكليف غير متاح"
        else:
            datef = date(dat.year + 2, dat.month, dat.day)
            return datef

    def get_grad_arab(self, a):
        if (a == "PESA"):
            return " أستاذ التعليم العالي مساعد"
        elif (a == "PH"):
            return "أستاذ مؤهل"
        else:
            return "أستاذ التعليم العالي"

    def get_categori_arab(self, cat):
        if (cat == "A"):
            return "أ"
        elif (cat == "B"):
            return "ب"
        elif (cat == "C"):
            return "ج"
        else:
            return "د"

    def get_grade_affec(self, grad):
        if (grad == "PESA"):
            return " أستاذ التعليم العالي مؤهل"
        elif (grad == "PH"):
            return "أستاذ التعليم العالي"

    def get_grad_indic(self, indic, grad):
        if (grad == "PESA"):
            query = """select "indice"  from ensaf_indice WHERE grade='%s' AND indice>=%s""" % (
                "PH", indic)
            self.env.cr.execute(query)
            indice = self.env.cr.fetchall()

            if (indice != []):
                return indice[0][0]
            else:
                return []
        elif (grad == "PH"):
            query = """select "indice"  from ensaf_indice WHERE grade='%s' AND indice>=%s""" % (
                "PES", indic)
            self.env.cr.execute(query)
            indice = self.env.cr.fetchall()

            if (indice != []):
                return indice[0][0]
            else:
                return []

    def get_grad_echlon(self, indic, grad):
        if (grad == "PESA"):
            query = """select "echelon"  from ensaf_indice WHERE grade='%s' AND indice=%s""" % (
                "PH", self.get_grad_indic(indic, grad))
            self.env.cr.execute(query)
            indice = self.env.cr.fetchall()

            if (indice != []):
                return indice[0][0]
            else:
                return []
        elif (grad == "PH"):
            query = """select "echelon"  from ensaf_indice WHERE grade='%s' AND indice=%s""" % (
                "PES", self.get_grad_indic(indic, grad))
            self.env.cr.execute(query)
            indice = self.env.cr.fetchall()

            if (indice != []):
                return indice[0][0]
            else:
                return []

    def get_grad_categorie(self, indic, grad):
        if (grad == "PESA"):
            query = """select "categorie"  from ensaf_indice WHERE grade='%s' AND indice=%s""" % (
                "PH", self.get_grad_indic(indic, grad))
            self.env.cr.execute(query)
            indice = self.env.cr.fetchall()

            if (indice != []):
                return self.get_categori_arab(indice[0][0])
            else:
                return []
        elif (grad == "PH"):
            query = """select "categorie"  from ensaf_indice WHERE grade='%s' AND indice=%s""" % (
                "PES", self.get_grad_indic(indic, grad))
            self.env.cr.execute(query)
            indice = self.env.cr.fetchall()

            if (indice != []):
                return self.get_categori_arab(indice[0][0])
            else:
                return []

    def check_date(self, date1, date2):
        date1 = str(date1)
        date2 = str(date2)
        if (date2 != "None"):
            if (date1 != "None"):
                dateRe = datetime.strptime(date2, "%Y-%m-%d")
                datePr = datetime.strptime(date1, "%Y-%m-%d")
                datef = date(datePr.year, datePr.month, datePr.day)
                datel = date(dateRe.year, dateRe.month, dateRe.day)
                delta = datef - datel
                return delta.days
        else:
            return 1

    def actualise(self):
        query = """select "id" from ensaf_enseignant"""
        self.env.cr.execute(query)
        enseig = self.env.cr.fetchall()
        for row in enseig:
            query = """UPDATE ensaf_enseignant SET proposition_echlon= %s,proposition_categorie= %s,proposition_grade= %s,proposition_titulaire= %s  WHERE id=%s""" % (
                False, False, False, False, row[0])
            self.env.cr.execute(query)

        # message = ("Connection Test Successful!")
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'message': message,
        #         'type': 'success',
        #         'sticky': False,
        #     }
        # }

    def _echelon_position(self, today):
        query = """select "id" , "dateEffetEchel" from ensaf_enseignant"""
        self.env.cr.execute(query)
        enseig = self.env.cr.fetchall()
        for row in enseig:
            time = str(row[1])
            if (self.check_date(today, time) >= 730):
                query = """UPDATE ensaf_enseignant SET proposition_echlon= %s WHERE id=%s""" % (True, row[0])
                self.env.cr.execute(query)

    # def _article14(self, today):
    #     query = """select "id" , "echelon" , "categorie" ,"dateEffetEchel","grade" from ensaf_enseignant"""
    #     self.env.cr.execute(query)
    #     enseig = self.env.cr.fetchall()
    #     for row in enseig:
    #         echeldate = str(row[3])
    #         echelon = row[1]
    #         categori = str(row[2])
    #         vgrade = str(row[3])

    #         match echelon:
    #             case 3:
    #                 if (self.check_date(today, echeldate) >= 1095):
    #                     query = """UPDATE ensaf_enseignant SET proposition_categorie= %s WHERE id=%s""" % (True, row[0])
    #                     self.env.cr.execute(query)
    #                     query = """UPDATE ensaf_enseignant SET system= '%s' WHERE id=%s""" % ('rapide', row[0])
    #                     self.env.cr.execute(query)
    #                 elif (self.check_date(today, echeldate) >= 730):
    #                     query = """UPDATE ensaf_enseignant SET proposition_categorie= %s WHERE id=%s""" % (True, row[0])
    #                     self.env.cr.execute(query)
    #                     query = """UPDATE ensaf_enseignant SET system= '%s' WHERE id=%s""" % ('exceptionnel', row[0])
    #                     self.env.cr.execute(query)
    #             case 4:
    #                 if (self.check_date(today, echeldate) > 729):
    #                     query = """UPDATE ensaf_enseignant SET proposition_categorie= %s WHERE id=%s""" % (True, row[0])
    #                     self.env.cr.execute(query)
    #                     query = """UPDATE ensaf_enseignant SET system= '%s' WHERE id=%s""" % ('normale', row[0])
    #                     self.env.cr.execute(query)

    #                 elif (self.check_date(today, echeldate) >= 365):
    #                     query = """UPDATE ensaf_enseignant SET proposition_categorie= %s WHERE id=%s""" % (True, row[0])
    #                     self.env.cr.execute(query)
    #                     query = """UPDATE ensaf_enseignant SET system= '%s' WHERE id=%s""" % ('rapide', row[0])
    #                     self.env.cr.execute(query)
    #                 else:
    #                     query = """UPDATE ensaf_enseignant SET proposition_categorie= %s WHERE id=%s""" % (True, row[0])
    #                     self.env.cr.execute(query)
    #                     query = """UPDATE ensaf_enseignant SET system= '%s' WHERE id=%s""" % ('exceptionnel', row[0])
    #                     self.env.cr.execute(query)

    def _titulaire_proposition(self, today):
        query = """select "id" , "dateRecru", "statut" from ensaf_enseignant"""
        self.env.cr.execute(query)
        enseig = self.env.cr.fetchall()
        for row in enseig:
            dateRecr = str(row[1])
            statu = str(row[2])
            if (statu == "stagiaire"):
                if (self.check_date(today, dateRecr) >= 730):
                    query = """UPDATE ensaf_enseignant SET proposition_titulaire= %s WHERE id=%s""" % (True, row[0])
                    self.env.cr.execute(query)

    def _grade_proposition(self, today):
        query = """select "id" , "statut","echelon","grade" ,"dateRecru", "datePH" from ensaf_enseignant"""
        self.env.cr.execute(query)
        enseig = self.env.cr.fetchall()
        for row in enseig:
            statu = row[1]
            echlo = row[2]
            v_grade = row[3]
            date_echel = row[4]
            date_PH = row[5]
            if (v_grade == "PESA"):
                if (self.check_date(today, date_echel) >= 1460):
                    print(date_echel)
                    query = """UPDATE ensaf_enseignant SET proposition_grade= %s WHERE id=%s""" % (True, row[0])
                    self.env.cr.execute(query)
            if (v_grade == "PH"):
                if (self.check_date(today, date_PH) >= 2190):
                    query = """UPDATE ensaf_enseignant SET proposition_grade= %s WHERE id=%s""" % (True, row[0])
                    self.env.cr.execute(query)

    def notification(self):
        self.actualise()
        query = """select "datePresid"  from date_presidence_wizard"""
        self.env.cr.execute(query)
        date = self.env.cr.fetchall()
        x = len(date) - 1
        s = str(date[x][0])
        today = datetime.strptime(s, "%Y-%m-%d").date()
        self._titulaire_proposition(today)
        self._echelon_position(today)
        self._article14(today)
        self._grade_proposition(today)

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     self._titulaire_proposition()
    #     self._echelon_position()
    #     self._article14()
    #     # self.notification()
    #     self._grade_proposition()
    #     return res
