# ERPNext POS Extensions - BaseN

Extensiones POS para ERPNext: vales, ticket regalo y personalizaciones para BaseN.

> **Última actualización**: 2026-07-18 — v0.1.0

## Funcionalidades

### Vale automático en devoluciones POS

Al crear una devolución desde el POS, automáticamente añade `Vale` como método de pago
por defecto (con el importe total) y `Efectivo` como alternativa (0€).

El vendedor elige en el POS:
- **Si quiere Vale**: no toca nada, pulsa Finalizar
- **Si quiere efectivo**: pone el importe en Efectivo y 0 en Vale

### Setup inicial

Al instalar la app, se crean automáticamente:
- Cuenta contable `Vales emitidos pendientes de canje` (Pasivo)
- Modo de pago `Vale` vinculado a la cuenta
- `Vale` añadido a los perfiles POS existentes (Caja1, Caja2)

## Instalación

```bash
# Desde el bench:
bench get-app https://github.com/soporteLyra/basenext-custom-app
bench --site tu-sitio.frappe.cloud install-app erpnext_pos_extensions
```

O desde Frappe Cloud Dashboard:
1. Apps → Install from Git
2. Pegar la URL del repositorio: `https://github.com/soporteLyra/basenext-custom-app`
3. Seleccionar el sitio
4. Instalar

## Desarrollo

### Estructura

```
erpnext_pos_extensions/
├── setup.py
├── erpnext_pos_extensions/
│   ├── __init__.py
│   ├── hooks.py           ← Event hooks
│   ├── install.py         ← Setup inicial
│   ├── patches.txt
│   ├── requirements.txt
│   └── events/
│       ├── __init__.py
│       └── sales_invoice.py  ← Lógica de vales
```
