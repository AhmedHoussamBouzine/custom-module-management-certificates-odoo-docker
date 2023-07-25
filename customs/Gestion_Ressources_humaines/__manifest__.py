# -*- coding: utf-8 -*-
{
    'name': 'Gestion du personnel',
    'version': '1.0.0',
    'Sequence': -1000,
    'category': 'Gestion',
    'summary': 'Gestion du personnel ENSAF',
    'description': """Gestion du personnel ENSAF""",
    'depends': ["mail","gestion_attestations"],
    'data': [
        'security/ir.model.access.csv',
        'wizard/date_presidence_view.xml',
        'data/ensaf.enseignant.csv',
        'views/menu.xml',
        'views/enseignant_view.xml',
        'views/administratif_view.xml',
        'views/indice_view.xml',
        'views/comité_view.xml',
        'views/documentsEnsg_view.xml'
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
