# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe

def after_install():
    _crear_cuenta_vale()
    _crear_modo_pago_vale()
    _actualizar_perfiles_pos()
    print("✅ App instalada correctamente")

def _crear_cuenta_vale():
    if frappe.db.exists("Account", "Vales emitidos pendientes de canje - BaseN"):
        return
    parent = frappe.db.get_value("Account", {"company": "BASENext", "root_type": "Liability", "is_group": 1, "account_name": "Pasivo circulante"})
    if not parent:
        return
    frappe.get_doc({
        "doctype": "Account", "account_name": "Vales emitidos pendientes de canje",
        "company": "BASENext", "parent_account": parent,
        "root_type": "Liability", "account_type": "Payable",
        "is_group": 0, "account_currency": "EUR",
    }).insert(ignore_permissions=True)

def _crear_modo_pago_vale():
    if frappe.db.exists("Mode of Payment", "Vale"):
        return
    frappe.get_doc({
        "doctype": "Mode of Payment", "mode_of_payment": "Vale",
        "enabled": 1, "type": "General",
        "accounts": [{"company": "BASENext", "default_account": "Vales emitidos pendientes de canje - BaseN"}],
    }).insert(ignore_permissions=True)

def _actualizar_perfiles_pos():
    for pos_name in ["Caja1 Zaragoza", "Caja2 Madrid"]:
        if not frappe.db.exists("POS Profile", pos_name):
            continue
        pos = frappe.get_doc("POS Profile", pos_name)
        if any(p.mode_of_payment == "Vale" for p in (pos.get("payments") or [])):
            continue
        pos.append("payments", {"mode_of_payment": "Vale", "default": 0, "allow_in_returns": 1})
        pos.save(ignore_permissions=True)
