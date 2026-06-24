import frappe

def create_testing_doc():
    test_doc = frappe.new_doc("Testing")

    test_doc.test1 = "Hello"
    test_doc.test2 = "Frappe 5"
    test_doc.test3 = 100
    test_doc.test4 = frappe.utils.today()

    test_doc.insert(ignore_permissions=True)


def validate_task(doc, method):
    create_testing_doc()
    frappe.msgprint("Testing document created")