{
  'name': 'Estacionamiento',
  'version': '1.0',
  'author': 'Ramiro',
  'depends': ['base'],
  'description': 'Módulo de estacionamiento.',
  'category': 'Sales',
  'data': [
    'security/ir.model.access.csv',
    'views/estacionamiento_cliente_view.xml',
    'views/estacionamiento_vehiculo_view.xml',
    'views/estacionamiento_lugar_view.xml',
    'views/estacionamiento_movimiento_view.xml',
    'views/estacionamiento_mensualidad_view.xml',
    'data/sequence.xml'
  ],
  'installable': True,
  'application': True,
  'icon': '/tienda/static/img/icon.png'
}