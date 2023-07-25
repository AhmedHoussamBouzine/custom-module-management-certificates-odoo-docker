from odoo import api, fields, models
import arabic_reshaper
from datetime import datetime
import locale



class Departement(models.Model):
    _name = "ensaf.departement"
    _description = "ENSAF Departement"

    name = fields.Selection([
        ('G E I', 'G E I'),
        ('G.INDUS', 'G.INDUS'),
        ('Génie des systèmes intelligents', 'Génie des systèmes intelligents'),
        ('Génie mathématique appliquées', 'Génie mathématique appliquées'),
        ('Intelligence économique langues et soft-skils', 'Intelligence économique langues et soft-skils'),
        ('Sciences des données et systèmes communicants', 'Sciences des données et systèmes communicants')
    ], string="Nom du département")


class Comite(models.Model):
    _name = "ensaf.comite"
    _description = "ENSAF comite"

    datecomite = fields.Date(string="Date de commission")
    type = fields.Selection([('titularisation', 'Titularisation'), ('avancement', 'Avancement')], string="type")
    grade = fields.Selection([('PES', 'PES'), ('PH', 'PH'), ('PESA', 'PESA')], string="Grade")
    categorie = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], string="Catégorie")
    echelon = fields.Integer(string="Echelon")
    departement_ids = fields.Many2many('ensaf.departement', string="Départements")
    enseignant_ids=fields.One2many('ensaf.comite.enseignant','comite_id',string="enseignants")
    membre_id_ids = fields.One2many('ensaf.comite.membres', 'membre_id', string="Membres de comités")


    def search_indice(self):
        related_model = self.env['ensaf.indice']
        domain = []
        domain += [('grade', '=', self.grade)]
        domain += [('echelon', '=', self.echelon)]
        domain += [('categorie', '=', self.categorie)]
        related_records = related_model.search(domain)
        return related_records.indice


    def search_related_records(self):
        related_model = self.env['ensaf.enseignant']
        domain = []
        domain += [('departement', 'ilike', self.departement)]
        domain += [('indiceActu', '>=', self.search_indice())]
        related_records = related_model.search(domain)
        return related_records

    def search_directeurs_records(self):
        related_model = self.env['ensaf.enseignant']
        domain = []
        domain += [('fonction', 'ilike', "Directeur")]
        related_records = related_model.search(domain)
        return related_records

    def get_Selected_Enseignanat(self):
        comite_record = self.env['ensaf.comite'].browse(self.id)
        selected_departments = comite_record.enseignant_ids
        department_names = selected_departments.mapped('departement')
        for department_name in department_names:
            print(department_name)
            department = self.env['ensaf.departement'].search([('name', 'ilike', department_name)], limit=1)
            if department:
                self.departement_ids = [(4, department.id, 0)]




        # selected_records = self.enseignant_ids
        # unique_departements = set()
        # departement_model = self.env['ensaf.departement']
        # for record in selected_records:
        #     unique_departements.add(record.departement)
        # # Process the unique departements and add them to departement_ids
        # departement_ids = []
        # for unique_departement in unique_departements:
        #     departement = departement_model.search([('name', '=', unique_departement)])
        #     if departement:
        #         departement_ids.append((4, departement.id))
        # self.departement_ids = departement_ids


    def get_Selected_chefdepartemet(self):
        comite_record = self.env['ensaf.comite'].browse(self.id)
        selected_departments = comite_record.departement_ids
        for department in selected_departments:
            related_model = self.env['ensaf.enseignant']
            domain = []
            domain += [('departement', 'ilike', department.name)]
            domain += [('activite', 'ilike', 'chef de département')]
            related_records = related_model.search(domain)
            child = self.env['ensaf.comite.membres'].create({
                'enseignant_id': related_records.id,
            })
            self.membre_id_ids += child


    def my_button_action(self):
        # self.get_Selected_Enseignanat()
        for record in self.search_directeurs_records():
            child = self.env['ensaf.comite.membres'].create({
                'enseignant_id': record.id,
            })
            self.membre_id_ids+=child
        self.get_Selected_chefdepartemet()


    def split_table(self,table):
        # Initialize empty tables
        table = sorted(table, key=lambda x: x['id'])
        table1 = []
        table2 = []
        table3 = []
        # Iterate over records and split into tables
        counter = 0
        for record in table:
            counter += 1
            if counter % 3 == 1:
                table1.append(record)
            elif counter % 3 == 2:
                table2.append(record)
            elif counter % 3 == 0:
                table3.append(record)
        # Return the resulting tables as a tuple
        return table1,table2,table3

    def get_grad_arab(self,a):
        if(a=="PESA"):
            return " أستاذ التعليم العالي مساعد"
        elif(a=="PH"):
            return "أستاذ مؤهل"
        else:
            return "أستاذ التعليم العالي"

    def get_categori_arab(self,cat):
        if(cat=="A"):
            return "أ"
        elif(cat=="B"):
            return "ب"
        elif(cat=="C"):
            return "ج"
        else:
            return "د"

    def get_type_arab(self,type):
        if (type == "Titularisation"):
            return "الترسيم"
        else:
            return "التسمية"

    def get_activite_arab(self,active,grad):
        if(active == "ENSEIGNEMENT"):
            return self.get_grad_arab(grad)
        elif(active == "Directeur "):
            return "مدير المدرسة الوطنية للعلوم التطبيقية بفاس"
        elif (active == "Directeur Adjoint chargé de la recherche scientifique et coopération"):
            return "المدير المساعد المكلف بالبحث العلمي والتعاون"
        elif (active == "Directeur Adjoint chargé des affaires académiques et pédagogiques"):
            return "المدير المساعد المكلف بالشؤون الأكاديمية والبيداغوجية"
        elif(active == "chef de département Génie électrique & informatique"):
            return "رئيس شعبة الهندسة الكهربائية و المعلوماتية"


class ComiteEnseignant(models.Model):
    _name = "ensaf.comite.enseignant"
    _description = "ENSAF comite enseignants"

    enseignant_id=fields.Many2one('ensaf.enseignant')
    comite_id=fields.Many2one('ensaf.comite', string="comite")
    nomAr = fields.Char(string="Nom",related='enseignant_id.nomAr')
    prenomAr = fields.Char(string="Prenom",related='enseignant_id.prenomAr')
    grade = fields.Selection(string="Grade",related='enseignant_id.grade')
    departement = fields.Char(string="Departement", related='enseignant_id.departement')





class ComiteMembres(models.Model):
    _name = "ensaf.comite.membres"
    _description = "ENSAF comite membres"

    enseignant_id=fields.Many2one('ensaf.enseignant')
    membre_id=fields.Many2one('ensaf.comite', string="comite")
    nomAr = fields.Char(string="Nom ",related='enseignant_id.nomAr')
    prenomAr = fields.Char(string="Prenom",related='enseignant_id.prenomAr')
    grade = fields.Selection(string="Grade",related='enseignant_id.grade')
    activ = fields.Char(string="Activite", related='enseignant_id.activite')
    categorie = fields.Selection(string="Categorie",related='enseignant_id.categorie')
    echelon = fields.Integer(string="Echelon",related='enseignant_id.echelon')
    departement = fields.Char(string="Departement", related='enseignant_id.departement')



