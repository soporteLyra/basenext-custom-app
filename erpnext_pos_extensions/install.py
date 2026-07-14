# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe

def after_install():
    """
    Setup inicial tras instalar la app.
    Crea los componentes necesarios si no existen.
    """
    _crear_cuenta_vale()
    _crear_modo_pago_vale()
    _actualizar_perfiles_pos()
    print("✅ basenext_custom_app instalada correctamente")


def _crear_cuenta_vale():
    """Crear cuenta pasivo 'Vales emitidos pendientes de canje'."""
    company = "BASENext"
    account_name = "Vales emitidos pendientes de canje"
    account_id = f"{account_name} - BaseN"

    if frappe.db.exists("Account", account_id):
        print(f"  ⚠️  Cuenta '{account_id}' ya existe")
        return

    # Buscar parent account bajo Pasivo circulante
    parent = frappe.db.get_value("Account", {
        "company": company,
        "root_type": "Liability",
        "is_group": 1,
        "account_name": "Pasivo circulante"
    })

    if not parent:
        print("  ❌ No se encontró 'Pasivo circulante'")
        return

    account = frappe.get_doc({
        "doctype": "Account",
        "account_name": account_name,
        "company": company,
        "parent_account": parent,
        "root_type": "Liability",
        "account_type": "Payable",
        "is_group": 0,
        "account_currency": "EUR",
    })
    account.insert(ignore_permissions=True)
    print(f"  ✅ Cuenta '{account_id}' creada")


def _crear_modo_pago_vale():
    """Crear modo de pago 'Vale'."""
    if frappe.db.exists("Mode of Payment", "Vale"):
        print("  ⚠️  Modo de pago 'Vale' ya existe")
        return

    mop = frappe.get_doc({
        "doctype": "Mode of Payment",
        "mode_of_payment": "Vale",
        "enabled": 1,
        "type": "General",
        "accounts": [{
            "company": "BASENext",
            "default_account": "Vales emitidos pendientes de canje - BaseN",
        }],
    })
    mop.insert(ignore_permissions=True)
    print("  ✅ Modo de pago 'Vale' creado")


def _actualizar_perfiles_pos():
    """Añadir 'Vale' a los perfiles POS existentes."""
    for pos_name in ["Caja1 Zaragoza", "Caja2 Madrid"]:
        if not frappe.db.exists("POS Profile", pos_name):
            print(f"  ⚠️  POS Profile '{pos_name}' no existe")
            continue

        pos = frappe.get_doc("POS Profile", pos_name)
        payments = pos.get("payments") or []

        # Verificar si ya tiene Vale
        if any(p.mode_of_payment == "Vale" for p in payments):
            print(f"  ⚠️  '{pos_name}' ya tiene Vale")
            continue

        # Añadir Vale
        pos.append("payments", {
            "mode_of_payment": "Vale",
            "default": 0,
            "allow_in_returns": 1,
        })
        pos.save(ignore_permissions=True)
        print(f"  ✅ Vale añadido a '{pos_name}'")
