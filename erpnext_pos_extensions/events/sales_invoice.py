# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def before_insert(doc, method):
    if doc.get("is_return") and doc.get("pos_profile"):
        total = abs(doc.get("grand_total") or 0)
        if total > 0:
            payments = doc.get("payments") or []
            tiene_vale = any(p.get("mode_of_payment") == "Vale" for p in payments)
            if not tiene_vale:
                doc.set("payments", [
                    {"mode_of_payment": "Vale", "amount": total, "base_amount": total, "default": 1},
                    {"mode_of_payment": "Efectivo", "amount": 0, "base_amount": 0, "default": 0},
                ])
