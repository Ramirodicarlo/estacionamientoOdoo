# Estacionamiento - Módulo Odoo

Este es un módulo personalizado desarrollado para la gestión de un estacionamiento dentro del sistema Odoo. Permite registrar clientes, vehículos, movimientos y abonos mensuales de una manera eficiente y automatizada.

## 📦 Contenido del módulo

- Gestión de vehículos con control de patentes únicas y validaciones.
- Registro de clientes y asociación con vehículos.
- Control de movimientos de entrada y salida de vehículos.
- Asignación de lugares y liberación automática al cerrar un movimiento.
- Gestión de mensualidades con control de vigencia y estado.
- Vistas personalizadas y menú integrado en el backend de Odoo.


## 🧱 Estructura
estacionamiento/
├── init.py
├── manifest.py
├── data/
│ └── sequence.xml
├── models/
│ ├── init.py
│ ├── estacionamiento_cliente.py
│ ├── estacionamiento_lugar.py
│ ├── estacionamiento_mensualidad.py
│ ├── estacionamiento_movimiento.py
│ └── estacionamiento_vehiculo.py
├── security/
│ └── ir.model.access.csv
├── static/
├── views/
│ ├── estacionamiento_cliente_view.xml
│ ├── estacionamiento_lugar_view.xml
│ ├── estacionamiento_mensualidad_view.xml
│ ├── estacionamiento_movimiento_view.xml
│ └── estacionamiento_vehiculo_view.xml

## 🧱 Logica de los Modulos

-Model cliente: Modelo de gestion de clientes sencillo donde solo valida el cuit que sea numerico y con longiutd de 11. Muestra vehiculos asignados
-Model vehiculo: Modelo de gestion de vehicuos en donde valida formatos de patentes aaxxaa o aaaxxx y que sean unicas. Ademas muestra relacion con cliente y tiene estados para saber si esta estacionado el vehiculo y si tiene una mensualidad activa.
-Model lugar: Modelo de gestion de lugares sencillo. Se asigna un vehiculo y figura como activo, son unicos y no se puede asignar el mismo vehicul a otro lugar. Cuando se registra un movimiento de salida, este pasa a estar disponible
-Model movimiento: Modelo de gestion de movimientos. Registra entrada y salida de vehiculos. Valida fechas para que la salida no sea ni igual ni menor al ingreso y que los estados correspondan a si hay fecha de egreso o no.
-Model mensualidad: Modelo de gestion de mensualidad. Registra mensualidades unicas avticas por vehiculo. Permite cargar una mensualdiad nueva si el vehiculo no posee ninguna activa. esto cambie el estado en vehiculo.

## Notas
- Decidi dejar hasta aca el sistema ya que sino me iba a extender demasiado con los requerimientos. Preferi tener validado todo lo mejor posible antes que seguir escalando en cuestiones no requeridas. Pero es posible escalarlo mas