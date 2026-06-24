// Copyright (c) 2026, Divin and contributors
// For license information, please see license.txt

frappe.ui.form.on("Testing", {
	button(frm) {
        frappe.call({
            method: "custom_module.api.hello",
            callback: function(r) {
                console.log(r.message);
                frappe.msgprint(r.message)
            }
        });
	}
});
