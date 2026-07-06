import frappe
import requests
from frappe.model.document import Document

class TaskAllocation(Document):
    def on_submit(self):
        self.notify_telegram()

    def notify_telegram(self):
        bot_token = frappe.conf.get("telegram_bot_token")
        chat_id = frappe.conf.get("telegram_chat_id")

        message = self.build_message()

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        try:
            requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=5)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Telegram Notification Failed")

    def build_message(self):
        lines = [f"✅ *Task Allocation Submitted*", f"Name: {self.name}", ""]

        # Standard metadata
        lines.append(f"Created By: {self.owner}")
        lines.append(f"Created On: {frappe.utils.format_datetime(self.creation)}")
        lines.append(f"Last Modified By: {self.modified_by}")
        lines.append(f"Last Modified On: {frappe.utils.format_datetime(self.modified)}")
        lines.append("")

        # All regular fields (skip system/meta fields already shown, and empty values)
        skip_fields = {
            "name", "owner", "creation", "modified", "modified_by",
            "docstatus", "idx", "doctype", "parent", "parentfield",
            "parenttype", "_user_tags", "_comments", "_assign", "_liked_by"
        }

        for field in self.meta.fields:
            fieldname = field.fieldname
            if fieldname in skip_fields:
                continue
            if field.fieldtype in ("Table", "Table MultiSelect"):
                continue  # handled separately below
            if field.fieldtype in ("Section Break", "Column Break", "HTML", "Button"):
                continue

            value = self.get(fieldname)
            if value in (None, "", 0, False):
                continue

            label = field.label or fieldname
            lines.append(f"{label}: {value}")

        # Child tables
        for field in self.meta.fields:
            if field.fieldtype != "Table":
                continue
            child_rows = self.get(field.fieldname)
            if not child_rows:
                continue
            lines.append("")
            lines.append(f"--- {field.label or field.fieldname} ---")
            for i, row in enumerate(child_rows, start=1):
                row_parts = []
                for cf in row.meta.fields:
                    if cf.fieldtype in ("Section Break", "Column Break", "HTML", "Button"):
                        continue
                    val = row.get(cf.fieldname)
                    if val in (None, "", 0, False):
                        continue
                    row_parts.append(f"{cf.label or cf.fieldname}: {val}")
                lines.append(f"Row {i}: " + ", ".join(row_parts))

        return "\n".join(lines)

