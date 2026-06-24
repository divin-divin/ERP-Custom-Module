import frappe



@frappe.whitelist(allow_guest=True)
def get_task_value(data):
    tasks=frappe.db.get_value(
        "Task Allocation",
        {"name":data,
         "employee":"HR-EMP-00001"},
         "employee"
    )
    return(tasks)


@frappe.whitelist(allow_guest=True)
def get_tasks_all(data):
    tasks=frappe.db.get_all(
        "Task Allocation",
        filters={"name":data,
                 "employee":"HR-EMP-00001"},
        fields=["employee_name","date","employee"]
    )
    return(tasks)

@frappe.whitelist(allow_guest=True)
def get_task_doc(data):
    task=frappe.get_doc(
        "Task Allocation",
        data
    )
    tasks_child=[]
    for i in task.task_allocation_table:
        if i.task_name == "testttt":
            tasks_child.append({
                "name":i.task_name
            })
    return(tasks_child)


@frappe.whitelist(allow_guest=True)
def get_task_list(data):
    task=frappe.db.get_list(
        "Task Allocation",
        fields=["employee","employee_name","date"],
        filters={"name":data}
    )
    return(task)



@frappe.whitelist(allow_guest=True)
def create_task_(employee,task_name):
    new=frappe.new_doc("Task Allocation")
    new.employee=employee
    new.append("task_allocation_table",
               {"task_name":task_name}

    )
    new.insert()

    return (new.name)


import frappe

import frappe

@frappe.whitelist()
def hello():
    session_user = frappe.session.user
    return f"Hi {session_user}, this is the Original API"


@frappe.whitelist()
def new_hello():
    session_user = frappe.session.user
    return f"Hi {session_user}, this is the Overridden API"





import frappe
@frappe.whitelist(allow_guest=True)
def create_task(doc, method):
    new = frappe.new_doc("Task Allocation")
    new.employee = "HR-EMP-00005"
    new.append(
        "task_allocation_table",
        {
            "task_name": "testing the hooks event"
        }
    )
    new.insert()
    return new.name








@frappe.whitelist(allow_guest=True)
def set_value(task_name):
    frappe.db.set_value(
        "Task Allocation",
        task_name,
        "date",
        "2029-03-02"
    )

    return("Date set Sucessfully")



@frappe.whitelist(allow_guest=True)
def check(task_name):
    if frappe.db.exists("Task Allocation",task_name):
        return("yes")
    else:
        return("no")
    

@frappe.whitelist(allow_guest=True)
def count(task_name):
    a=frappe.db.count("Task Allocation",task_name)

    return(a)

@frappe.whitelist(allow_guest=True)
def delete(task_name):

    frappe.delete_doc(
        "Task Allocation",
        task_name
    )

    return "Task deleted successfully"



import frappe
from frappe.auth import LoginManager

import frappe
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def login_and_get_token(username, password):
    try:
        # Convert username to email if needed
        if "@" not in username:
            email = frappe.db.get_value("User", {"username": username}, "name")
            if not email:
                frappe.throw("User not found")
            username = email

        login_manager = LoginManager()
        login_manager.authenticate(username, password)
        login_manager.post_login()

        user = frappe.get_doc("User", username)

        # Generate API keys if they don't exist
        if not user.api_key:
            user.api_key = frappe.generate_hash(length=15)
        if not user.api_secret:
            user.api_secret = frappe.generate_hash(length=15)

        user.save(ignore_permissions=True)

        # Generate token
        token = frappe.generate_hash(length=32)
        
        # Store token in cache for 24 hours
        frappe.cache.set_value(
            f"auth_token:{token}",
            {"user": username},
            expires_in_sec=86400
        )

        return {
            "status": "success",
            "user": user.name,
            "api_key": user.api_key,
            "api_secret": user.get_password("api_secret"),
            "token": token,
            "token_type": "Bearer"
        }

    except frappe.AuthenticationError:
        frappe.throw("Invalid Username or Password")






@frappe.whitelist(allow_guest=True)
def create_testing_doc():
    test_doc = frappe.new_doc("Testing")

    test_doc.test1 = "Hello"
    test_doc.test2 = "Frappe 5"
    test_doc.test3 = 100
    test_doc.test4 = frappe.utils.today()

    test_doc.insert(ignore_permissions=True)








# import frappe
# from frappe.utils import today

# @frappe.whitelist(allow_guest=True)
# def get_task_allocations():
#     data = frappe.get_all("Task Allocation", 
#         fields=["name", "employee", "employee_name", "date", "task_name"]
#     )
#     return data

# @frappe.whitelist(allow_guest=True)
# def get_single_task(name):
#     data = frappe.get_doc("Task Allocation", name)
#     return data

# def validate_task(doc, method):
#     frappe.msgprint("Task Allocation Validated!")


# @frappe.whitelist(allow_guest=True)
# def create_task_allocation():
#     doc = frappe.new_doc("Task Allocation")
#     doc.employee = "HR-EMP-00001"
#     doc.date = today()
#     doc.task_name = "testtt"
#     doc.insert(ignore_permissions=True)
#     frappe.db.commit()