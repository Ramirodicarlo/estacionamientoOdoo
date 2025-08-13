from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstacionamientoMensualidad(models.Model):
    _name = 'estacionamiento.mensualidad'
    _description = 'Abonos del estacionamiento'

    # No hace falta definir id, Odoo lo maneja automáticamente
    fecha_inicio = fields.Datetime(string='Fecha de Inicio')
    fecha_vencimiento = fields.Datetime(string='Fecha de Vencimiento')
    estado = fields.Selection(
        [('activa', 'Activa'), ('finalizada', 'Finalizada')],
        string='Estado',
        required=True,
        default='activa'
    )
    vehiculo_id = fields.Many2one('estacionamiento.vehiculo', string='Vehiculo',domain=[('mensualidad_activa', '=', False)] )

    @api.onchange('fecha_vencimiento')
    def _onchange_fecha_vencimiento(self):
        for record in self:
            if record.fecha_vencimiento:
                record.estado = 'finalizada'
            else:
                record.estado = 'activa'


    def _compute_display_name(self):
        for obj in self:
            obj.display_name = obj.id

    @api.constrains('vehiculo_id')
    def _check_vehiculo_unico(self):
        for record in self:
            if record.vehiculo_id:
                # Buscar si hay otro lugar asignado con el mismo vehiculo
                mensualidades_con_vehiculo = self.search([
                    ('vehiculo_id', '=', record.vehiculo_id.id),
                    ('id', '!=', record.id),
                    ('estado', '=', "activa")
                ])
                if mensualidades_con_vehiculo:
                    raise ValidationError(f"El vehículo '{record.vehiculo_id.patente}' ya está asignado a otra mensualidad activa.")
                
    @api.onchange('fecha_inicio', 'fecha_vencimiento')
    def _onchange_fechas(self):
        if self.fecha_inicio and self.fecha_vencimiento:
            if self.fecha_vencimiento <= self.fecha_inicio:
                return {
                    'warning': {
                        'title': "Fechas inválidas",
                        'message': "La fecha de vencimiento debe ser mayor a la fecha de inicio.",
                    }
                }
                    
    @api.constrains('fecha_inicio', 'fecha_vencimiento')
    def _check_fechas(self):
        for record in self:
            if record.fecha_inicio and record.fecha_vencimiento:
                if record.fecha_vencimiento <= record.fecha_inicio:
                    raise ValidationError("La fecha de vencimiento debe ser mayor a la fecha de inicio.")
                
    @api.constrains('estado', 'fecha_vencimiento')
    def _check_estado_vs_fecha_vencimiento(self):
        for record in self:
            # No permitir estado 'activa' si hay fecha de vencimiento
            if record.estado == 'activa' and record.fecha_vencimiento:
                raise ValidationError("No se puede marcar como activa una mensualidad que ya tiene fecha de vencimiento.")
            
            # No permitir estado 'finalizada' si NO hay fecha de vencimiento
            if record.estado == 'finalizada' and not record.fecha_vencimiento:
                raise ValidationError("No se puede marcar como finalizada una mensualidad sin una fecha de vencimiento.")