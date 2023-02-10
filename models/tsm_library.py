# -*- coding: utf-8 -*-
from odoo import models, fields, api

GENEROS = [
    ('Suspense', 'Suspenso'),
    ('Fiction', 'Ficción'),
    ('Adventure', 'Aventura'),
    ('Music', 'Música'),
    ('Manga', 'Manga')
]

ESTADOS = [
    ("ABIERTO", "ABIERTO"),
    ("CERRADO", "CERRADO")
]


class TsmBooks(models.Model):
    _name = 'tsm.books'
    _description = 'Libros'
    _rec_name = 'book_name'

    book_name = fields.Char('Libro', required=True)
    state = fields.Selection(ESTADOS, default="ABIERTO")
    genre = fields.Selection(GENEROS)
    date = fields.Date('Fecha de Publicación')
    author_id = fields.Many2one('tsm.author', 'Autor del Libro')
    total_books = fields.Integer('Total de Libros', compute='Total_Libros_compute')
    score = fields.One2many('tsm.score', 'book_id', 'Calificación del libro')
    adjunto = fields.Binary('Archivo')
    average = fields.Float()

    def button_reasign(self):
        wizard_id = self.env['reasign.data'].create([
            {
                'old_author': self.author_id.id,
                'old_genre': self.genre,
                'book_id': self.id}
        ])

        return {
            'view_mode': 'form',
            'res_model': 'reasign.data',
            'res_id': wizard_id.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self.env.context,
            'nodestroy': True
        }

    def button_abierto(self):
        self.state = "ABIERTO"

    def button_cerrado(self):
        self.state = "CERRADO"

    # FUNCIÓN PARA TRAER TODOS LOS LIBROS
    @api.multi
    def Total_Libros_compute(self):
        todos = self.env['tsm.books'].search([])
        self.total_books = len(todos)

    def score_average(self):
        suma = 0

        for i in self.score:
            suma = suma + i.score

        if len(self.score) == 0:
            self.average = 0
        else:
            self.average = suma / len(self.score)


ESTADOS = [
    ("ABIERTO", "ABIERTO"),
    ("CERRADO", "CERRADO")
]


class TsmAuthor(models.Model):
    _name = 'tsm.author'
    _description = 'Autor de libro'

    name = fields.Char('Nombre del Autor', required=True)
    birth_date = fields.Date('Fecha de Nacimiento', required=True)
    death_date = fields.Date('Fecha de Fallecimiento')
    description = fields.Char("Descripción")
    state = fields.Selection(ESTADOS, default="ABIERTO")
    book_id = fields.One2many('tsm.books', 'author_id', string='')

    def button_reasign(self):
        wizard_id = self.env['reasign.author'].create([
            {'old_name': self.name,
             'old_description': self.description,
             'author_id': self.id}
        ])

        return {
            'view_mode': 'form',
            'res_model': 'reasign.author',
            'res_id': wizard_id.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self.env.context,
            'nodestroy': True
        }

    def button_open(self):
        self.state = "ABIERTO"

    def button_close(self):
        self.state = "CERRADO"


class TsmScore(models.Model):
    _name = 'tsm.score'
    _description = 'Calificaciones del libro'

    score = fields.Integer('Calificación')
    book_id = fields.Many2one('tsm.books',  string="libro")
    user_id = fields.Many2one('res.users', 'calificado por')


class ReasignData(models.TransientModel):
    _name = 'reasign.data'

    new_author = fields.Many2one('tsm.author', 'Nuevo Autor')
    old_author = fields.Many2one('tsm.author', 'Viejo Autor')
    new_genre = fields.Selection(GENEROS)
    old_genre = fields.Selection(GENEROS)
    book_id = fields.Many2one('tsm.books')

    def do_reasign(self):
        if self.new_genre:
            self.book_id.genre = self.new_genre

        if self.new_author:
            self.book_id.author_id = self.new_author


class ReasignAuthor(models.TransientModel):
    _name = "reasign.author"

    new_name = fields.Char('Nuevo nombre')
    old_name = fields.Char('Antiguo Nombre')
    new_description = fields.Char('Nueva descripción')
    old_description = fields.Char("Antigua descripción")
    author_id = fields.Many2one('tsm.author', 'Author')

    def do_reasign(self):
        if self.new_name:
            self.author_id.name = self.new_name
        if self.new_description:
            self.author_id.description = self.new_description


class TsmCountBooks(models.Model):
    _name = "tsm.count.books"
    _description = "Contador Libros"

    book_line = fields.One2many('tsm.count.books.line', 'count_book_id', 'Detalle')

    def button_calculate(self):
        genres = [x[0] for x in GENEROS]

        self.book_line.unlink()

        genre_lines = []

        for gen in genres:
            books = self.env['tsm.books'].search([('genre', '=', gen)])
            if books:
                book_data  = {
                    'genre' : gen,
                    'qty' : len(books)
                }
                genre_lines.append(book_data)

        self.book_line = [(0,0,x) for x in genre_lines]



class TsmCountBooksLine(models.Model):
    _name = 'tsm.count.books.line'
    _description = 'Detalle libros'

    genre = fields.Selection(GENEROS, 'Genero')
    qty = fields.Integer('Cantidad')
    count_book_id = fields.Many2one('tsm.count.books')


class TsmCountAuthorBooks(models.Model):
    _name = "tsm.count.author.books"
    _description = "Contador Libros por Autor"

    author_line = fields.One2many('tsm.count.author.books.line', 'count_books_id', 'Author Line')

    def button_author_calculate(self):
        
        author = self.env['tsm.author'].search([])

        self.author_line.unlink()

        author_lines = []

        for a in author:                    
                                        # BUSCAMOS AUTHOR_ID PORQUE ES EL CAMPO QUE TIENE CADA LIBRO
            books = self.env['tsm.books'].search([('author_id', "=" , a.id)])

            if books:

                line_data = {
                    'name_author_id' : a.id,
                    'qty' : len(books)
                }
                author_lines.append(line_data)
            
        self.author_line = [(0,0,x) for x in author_lines]


class TsmCountAuthorBooksLine(models.Model):
    _name = "tsm.count.author.books.line"
    _description = "Detalle Author x libro"

    name_author_id = fields.Many2one('tsm.author')
    qty = fields.Integer('Cantidad Libros')
    count_books_id = fields.Many2one('tsm.count.author.books')

