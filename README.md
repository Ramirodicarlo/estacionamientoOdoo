# 🚗 Odoo Parking Management Module

Custom module developed in Odoo for managing a parking system, including vehicles, clients, parking spots, movements, and monthly subscriptions.

## 📌 Overview

This module provides a complete solution to manage a parking facility within Odoo ERP. It automates vehicle tracking, parking spot allocation, and subscription management, ensuring data consistency through validations and business rules.

## ⚙️ Key Features

- Vehicle management with unique license plate validation
- Client management with vehicle association
- Parking entry/exit tracking with date validations
- Automatic parking spot assignment and release
- Monthly subscription management with active status control
- Custom views and full integration into Odoo backend

## 🧠 Business Logic

The module includes multiple models with validations and relationships:

- **Client Model**
  - Validates CUIT format (numeric, 11 digits)
  - Displays associated vehicles

- **Vehicle Model**
  - Validates license plate formats (e.g., `AA123AA`, `AAA123`)
  - Ensures uniqueness
  - Tracks parking status and active subscription

- **Parking Spot Model**
  - Manages parking space availability
  - Prevents duplicate vehicle assignments
  - Automatically frees spots when a vehicle exits

- **Movement Model**
  - Handles vehicle entry and exit
  - Validates dates (exit must be after entry)
  - Controls vehicle state based on movement

- **Subscription Model**
  - Manages monthly parking subscriptions
  - Ensures only one active subscription per vehicle
  - Updates vehicle status automatically

## 🏗️ Project Structure

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


## 🛠️ Technologies Used

- Odoo (ERP Framework)
- Python
- XML (Views & Data)

## 📈 Possible Improvements

- Payment integration
- Reporting dashboard
- API exposure for external integrations
- Role-based access enhancements

## 📎 Notes

This project was intentionally scoped to focus on strong validation, data integrity, and core business logic rather than feature expansion.
