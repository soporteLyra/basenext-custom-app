# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Event handlers for Sales Invoice.
"""

def before_insert(doc, method):
    """
    Cuando se crea una devolución desde POS, añade 'Vale' como método de pago
    por defecto (importe total), dejando 'Efectivo' como alternativa (0€).

    El vendedor ve ambas opciones en el POS y elige:
      - Si quiere Vale: submit sin cambios
      - Si quiere efectivo: pone importe en Efectivo y 0 en Vale
    """
    if doc.get("is_return") and doc.get("pos_profile"):
        total = abs(doc.get("grand_total") or 0)
        if total > 0:
            # Comprobar si ya tiene Vale para no duplicar
            payments = doc.get("payments") or []
            tiene_vale = any(
                p.get("mode_of_payment") == "Vale" for p in payments
            )
            if not tiene_vale:
                # Reemplazar payments por Vale (total) + Efectivo (0)
                doc.set("payments", [
                    {
                        "mode_of_payment": "Vale",
                        "amount": total,
                        "base_amount": total,
                        "default": 1,
                    },
                    {
                        "mode_of_payment": "Efectivo",
                        "amount": 0,
                        "base_amount": 0,
                        "default": 0,
                    },
                ])
