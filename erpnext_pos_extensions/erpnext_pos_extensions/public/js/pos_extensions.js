/**
 * ERPNext POS Extensions - BaseN
 * Extensiones para el POS: vales automáticos, ticket regalo
 */

frappe.provide("erpnext_pos_extensions");

erpnext_pos_extensions.POSExtensions = class {
    constructor() {
        this.init();
    }

    init() {
        console.log("[BaseN] POS Extensions loaded");
        this.setup_vale_default();
    }

    /**
     * En devoluciones POS, pre-selecciona Vale como método de pago por defecto.
     * El hook before_insert ya lo hace en backend; este es el fallback en frontend.
     */
    setup_vale_default() {
        // El backend (events/sales_invoice.py) ya configura Vale por defecto.
        // Este JS es placeholder para futuras extensiones de UI en el POS.
        console.log("[BaseN] Vale default: handled by backend hook");
    }
};

// Inicializar cuando el DOM esté listo
$(document).ready(function () {
    new erpnext_pos_extensions.POSExtensions();
});
