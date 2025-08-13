from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError
import re

class EstacionamientoVehiculo(models.Model):
    _name = 'estacionamiento.vehiculo'
    
    _sql_constraints = [('patente_unique', 'unique(patente)', 'El número de patente ya está en uso. Debe ser única.')]


    patente = fields.Char(string='patente', required=True)
    estacionado = fields.Boolean(string='Estacionado', compute='_compute_estacionado', store=True, readonly=True)
    mensualidad_activa = fields.Boolean(string='Mensualidad Activa', compute='_compute_mensualidad_activa', store=True)

    cliente_id = fields.Many2one('estacionamiento.cliente', string='Duenio', required=True)
    mensualidad = fields.One2many('estacionamiento.mensualidad', 'vehiculo_id', string='Mensualidades', readonly=True)

    movimiento_ids = fields.One2many('estacionamiento.movimiento', 'vehiculo_id', string='Movimientos')

    def _compute_display_name(self):
        for obj in self:
            obj.display_name = obj.patente

    @api.depends('mensualidad.estado')
    def _compute_mensualidad_activa(self):
        for vehiculo in self:
            vehiculo.mensualidad_activa = any(m.estado == 'activa' for m in vehiculo.mensualidad)
            
    @api.depends('movimiento_ids.estado')
    def _compute_estacionado(self):
        for vehiculo in self:
            # Si alguno de sus movimientos está en estado 'abierto', estacionado = True
            abierto = any(mov.estado == 'abierto' for mov in vehiculo.movimiento_ids)
            vehiculo.estacionado = abierto

    @api.constrains('patente')
    def _check_patente(self):
        for record in self:
            if record.patente:
                patente = record.patente.strip()
                primeros_tres = patente[:3]

                if re.match(r'^[A-Za-z]{3}$', primeros_tres):
                    # Si los primeros 3 son letras, longitud debe ser 6
                    if len(patente) != 6:
                        raise ValidationError("Si los primeros 3 caracteres son letras, la patente debe tener 6 caracteres de longitud.")
                elif re.match(r'^[A-Za-z]{2}[0-9]$', primeros_tres):
                    # Si los primeros 2 son letras y el tercero es número, longitud debe ser 7
                    if len(patente) != 7:
                        raise ValidationError("Si los primeros 2 caracteres son letras y el tercero es número, la patente debe tener 7 caracteres de longitud.")
                    # Verificamos que el carácter 6 y 7 sean letras
                    if not (patente[5].isalpha() and patente[6].isalpha()):
                        raise ValidationError("Si los dos primeros son letras y el tercero un número, los caracteres 6 y 7 deben ser letras.")
                    pass