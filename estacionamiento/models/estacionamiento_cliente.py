from odoo import api, fields, models, exceptions

class EstacionamientoCliente(models.Model):
    _name = 'estacionamiento.cliente'
    _description = 'Clientes del estacionamiento'

    cuit = fields.Char('CUIT',required=True)
    nombre = fields.Char(string='Nombre')

    
    vehiculos = fields.One2many('estacionamiento.vehiculo', 'cliente_id', string='Vehículos',readonly=True)
  
    def _compute_display_name(self):
        for obj in self:
            obj.display_name = obj.nombre

    @api.constrains('cuit')
    def _check_cliente_cuit(self):
        for obj in self:
            if not obj.cuit or len(obj.cuit) != 11:
                raise exceptions.ValidationError('El cuit debe tener una longitud de 11 caracteres')
        for obj in self:
            if not obj.cuit.isdigit():
                raise exceptions.ValidationError('El cuit debe contener solo numeros')
