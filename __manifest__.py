# -*- coding: utf-8 -*-
{
    'name': 'Biblioteca',
    'version': '1.0',
    'website': 'https://www.driverp.com',
    'author': 'DrivErp',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': 'Modulo de libros',
    'depends': ['base'],
    'description': '''
        Descripcion blablablablablabla libros
    ''',
    'data': [
        'views/tsm_library_menus.xml',
        'views/tsm_library_views.xml',
        'views/tsm_author_views.xml',
        'views/tsm_score_views.xml',
        'views/tsm_count_books.xml',
        'views/tsm_count_author_books.xml',
        'report/pdf_author.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [],
    'test': [],
    'application': True,
}
