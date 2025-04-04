"""
Flex-Work Application Entry Point
"""
from app import app
from flask import request
from app.routes.auth import login_credentials, sign_up, logout
from app.routes.organizations import (
    create_organization, delete_organization, leave_organization,
    add_member, remove_member, get_organization_info, groups
)
from app.routes.inventory import inventory, add_inventory_item, delete_inventory_item, download_file, preview_file
from app.routes.bulletin import bulletin, handle_announcements
from app.routes.dashboard import dashboard, account_manager, update_profile
from app.routes.workpad import workpad, create_task, update_task_status, delete_task
from app.routes.work_groups import (
    create_work_group, get_user_groups, update_work_group, delete_work_group,
    get_group_details, add_item_to_group, remove_item_from_group
)

# Registering routes
app.route("/", methods=['GET', 'POST'])(login_credentials)
app.route("/sign_up", methods=['GET', 'POST'])(sign_up)
app.route("/logout", methods=['GET', 'POST'])(logout)
app.route("/dashboard")(dashboard)
app.route("/account_manager")(account_manager)
app.route("/update_profile", methods=['POST'])(update_profile)
app.route("/create_organization", methods=['POST'])(create_organization)
app.route("/delete_organization", methods=['POST'])(delete_organization)
app.route("/leave_organization", methods=['POST'])(leave_organization)
app.route("/add_member", methods=['POST'])(add_member)
app.route("/remove_member", methods=['POST'])(remove_member)
app.route("/groups")(groups)
app.route("/user_organizations/<int:org_id>/info")(get_organization_info)
app.route("/inventory")(inventory)
app.route("/add_inventory_item", methods=['POST'])(add_inventory_item)
app.route("/delete_inventory_item/<int:item_id>", methods=['DELETE'])(delete_inventory_item)
app.route("/download_file/<int:item_id>")(download_file)
app.route("/preview/<int:item_id>")(preview_file)
app.route("/bulletin")(bulletin)
app.route("/announcements", methods=['POST', 'DELETE'])(handle_announcements)
app.route("/workpad", methods=['GET', 'POST'])(workpad)
app.route("/tasks", methods=['POST'])(create_task)
app.route("/tasks/<task_id>/status", methods=['PUT'])(update_task_status)
app.route("/tasks/<task_id>", methods=['DELETE'])(delete_task)

# Work Groups routes
def handle_work_groups():
    if request.method == 'POST':
        return create_work_group()
    return get_user_groups()

app.route("/work_groups", methods=['GET', 'POST'])(handle_work_groups)
app.route("/work_groups/<int:group_id>", methods=['GET'])(get_group_details)
app.route("/work_groups/<int:group_id>", methods=['PUT'])(update_work_group)
app.route("/work_groups/<int:group_id>", methods=['DELETE'])(delete_work_group)
app.route("/work_groups/<int:group_id>/items", methods=['POST'])(add_item_to_group)
app.route("/work_groups/<int:group_id>/items/<int:item_id>", methods=['DELETE'])(remove_item_from_group)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)