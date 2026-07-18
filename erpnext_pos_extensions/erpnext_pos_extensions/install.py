# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe

COMPANY = "BASENext"


def after_install():
    if not frappe.db.exists("Company", COMPANY):
        print(f"⚠️  Compañía '{COMPANY}' no existe aún. Configura la compañía y ejecuta:")
        print(f"   bench --site {frappe.local.site} execute erpnext_pos_extensions.erpnext_pos_extensions.install.after_install")
        return

    _crear_cuenta_vale()
    _crear_modo_pago_vale()
    _actualizar_perfiles_pos()
    print("✅ App instalada correctamente")


def _crear_cuenta_vale():
    if frappe.db.exists("Account", f"Vales emitidos pendientes de canje - {COMPANY}"):
        return
    parent = frappe.db.get_value("Account", {
        "company": COMPANY, "root_type": "Liability",
        "is_group": 1, "account_name": "Pasivo circulante"
    })
    if not parent:
        print("⚠️  No se encontró cuenta padre 'Pasivo circulante'. Saltando creación de cuenta Vale.")
        return
    frappe.get_doc({
        "doctype": "Account", "account_name": "Vales emitidos pendientes de canje",
        "company": COMPANY, "parent_account": parent,
        "root_type": "Liability", "account_type": "Payable",
        "is_group": 0, "account_currency": "EUR",
    }).insert(ignore_permissions=True)
    print("✅ Cuenta 'Vales emitidos pendientes de canje' creada")


def _crear_modo_pago_vale():
    if frappe.db.exists("Mode of Payment", "Vale"):
        return
    cuenta = f"Vales emitidos pendientes de canje - {COMPANY}"
    if not frappe.db.exists("Account", cuenta):
        print(f"⚠️  Cuenta '{cuenta}' no existe. Saltando creación de modo de pago Vale.")
        return
    frappe.get_doc({
        "doctype": "Mode of Payment", "mode_of_payment": "Vale",
        "enabled": 1, "type": "General",
        "accounts": [{"company": COMPANY, "default_account": cuenta}],
    }).insert(ignore_permissions=True)
    print("✅ Modo de pago 'Vale' creado")


def _actualizar_perfiles_pos():
    for pos_name in ["Caja1 Zaragoza", "Caja2 Madrid"]:
        if not frappe.db.exists("POS Profile", pos_name):
            continue
        pos = frappe.get_doc("POS Profile", pos_name)
        if any(p.mode_of_payment == "Vale" for p in (pos.get("payments") or [])):
            continue
        pos.append("payments", {"mode_of_payment": "Vale", "default": 0, "allow_in_returns": 1})
        pos.save(ignore_permissions=True)
        print(f"✅ Perfil POS '{pos_name}' actualizado con modo de pago Vale")
