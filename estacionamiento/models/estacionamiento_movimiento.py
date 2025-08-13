from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstacionamientoMovimiento(models.Model):
    _name = 'estacionamiento.movimiento'
    _description = 'Movimiento de vehículos en el estacionamiento'

    fecha_ingreso = fields.Datetime(string='Fecha de Ingreso')
    fecha_salida = fields.Datetime(string='Fecha de Salida')
    estado = fields.Selection(
        [('abierto', 'Abierto'), ('cerrado', 'Cerrado')],
        string='Estado',
        required=True,
        default ='abierto'
    )

    lugar_id = fields.Many2one('estacionamiento.lugar', string='Lugar')  
    vehiculo_id = fields.Many2one('estacionamiento.vehiculo', string='Vehículo', compute='_compute_vehiculo_id', store=True)

    @api.onchange('lugar_id')
    def _onchange_lugar_id(self):
        if self.lugar_id and self.lugar_id.vehiculo_id:
            self.vehiculo_id = self.lugar_id.vehiculo_id
        else:
            self.vehiculo_id = False
            
    @api.depends('lugar_id')
    def _compute_vehiculo_id(self):
        for record in self:
            record.vehiculo_id = record.lugar_id.vehiculo_id if record.lugar_id else False

    def _compute_display_name(self):
        for obj in self:
            obj.display_name = f"Movimiento {obj.id}"
            
    @api.onchange('fecha_salida')
    def _onchange_fecha_salida(self):
        for record in self:
            if record.fecha_salida:
                record.estado = 'cerrado'
            else:
                record.estado = 'abierto'
            
                
    @api.onchange('fecha_ingreso', 'fecha_salida')
    def _onchange_fechas(self):
        if self.fecha_ingreso and self.fecha_salida:
            if self.fecha_salida <= self.fecha_ingreso:
                return {
                    'warning': {
                        'title': "Fechas inválidas",
                        'message': "La fecha de vencimiento debe ser mayor a la fecha de inicio.",
                    }
                }
                    
    @api.constrains('fecha_ingreso', 'fecha_salida')
    def _check_fechas(self):
        for record in self:
            if record.fecha_ingreso and record.fecha_salida:
                if record.fecha_salida <= record.fecha_ingreso:
                    raise ValidationError("La fecha de vencimiento debe ser mayor a la fecha de inicio.")
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._liberar_lugar_si_salida()
        return record

    def write(self, vals):
        res = super().write(vals)
        self._liberar_lugar_si_salida()
        return res

    def _liberar_lugar_si_salida(self):
        for movimiento in self:
            if movimiento.estado == 'cerrado' and movimiento.lugar_id :
                lugar = movimiento.lugar_id
                if lugar.vehiculo_id:
                    lugar.write({
                        'vehiculo_id': False,
                        'ocupado': False
                    })