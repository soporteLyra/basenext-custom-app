# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "erpnext_pos_extensions"
app_title = "ERPNext POS Extensions - BaseN"
app_publisher = "Lyra Informática"
app_description = "Extensiones POS para ERPNext: vales, ticket regalo y personalizaciones BaseN"
app_email = "jmpascual@lyra-informatica.es"
app_license = "MIT"

app_include_js = ["/assets/erpnext_pos_extensions/js/pos_extensions.js"]
app_include_css = ["/assets/erpnext_pos_extensions/css/pos_extensions.css"]

doc_events = {
    "Sales Invoice": {
        "before_insert": "erpnext_pos_extensions.erpnext_pos_extensions.events.sales_invoice.before_insert",
    }
}

fixtures = ["Custom Field", "Custom DocPerm", "Print Format", "Client Script", "Letter Head"]
after_install = "erpnext_pos_extensions.erpnext_pos_extensions.install.after_install"
