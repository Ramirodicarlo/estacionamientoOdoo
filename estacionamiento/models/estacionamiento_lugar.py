from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstacionamientoLugar(models.Model):
    _name = 'estacionamiento.lugar'
    _description = 'Lugares de estacionamiento'

    lugar_id = fields.Integer(string='ID lugar', required=True)
    ocupado = fields.Boolean(string='Ocupado', default=False)
    vehiculo_id = fields.Many2one('estacionamiento.vehiculo', string='Vehiculo')

    _sql_constraints = [
        ('lugar_id_unique', 'unique(lugar_id)', 'El número de lugar ya está en uso. Debe ser único.')
    ]

    @api.model
    def create(self, vals):
        if not vals.get('lugar_id'):
            last = self.search([], order='lugar_id desc', limit=1)
            next_id = last.lugar_id + 1 if last else 1
            if next_id > 10:
                raise ValidationError("No se pueden asignar más de 10 lugares.")
            vals['lugar_id'] = next_id
        return super().create(vals)

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        self.ocupado = bool(self.vehiculo_id)

    @api.constrains('vehiculo_id')
    def _check_vehiculo_unico(self):
        for record in self:
            if record.vehiculo_id:
                lugares_con_vehiculo = self.search([
                    ('vehiculo_id', '=', record.vehiculo_id.id),
                    ('id', '!=', record.id),
                    ('ocupado', '=', True)
                ])
                if lugares_con_vehiculo:
                    raise ValidationError(f"El vehículo '{record.vehiculo_id.patente}' ya está asignado a otro lugar ocupado.")

    @api.constrains('lugar_id')
    def _check_lugar_id_rango(self):
        for record in self:
            if record.lugar_id < 1 or record.lugar_id > 10:
                raise ValidationError("El número de lugar debe estar entre 1 y 10.")

    @api.depends('vehiculo_id')
    def _compute_display_name(self):
        for obj in self:
            obj.display_name = str(obj.lugar_id)
            
    @api.onchange('lugar_id')
    def _onchange_fechas(self):
        if self.lugar_id > 10:
                return {
                    'warning': {
                        'title': "Numero de Lugar inválidas",
                        'message': "El numero de lugar no puede ser mayor a 10.",
                    }
                }