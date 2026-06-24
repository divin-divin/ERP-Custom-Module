# Copyright (c) 2026, Divin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class TaskAllocation(Document):
    # def validate(self):
    #     if str(self.date) != today():
    #         frappe.throw("Only today's date is allowed!")
    def on_submit(self):
        frappe.msgprint("Thank you for submit the documhghgent")



@frappe.whitelist()
def data(employee,employee_name):
    frappe.msgprint(f"{employee} -----{employee_name}")