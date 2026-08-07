app_name = "sfpl_strip"
app_title = "SFPL Strip"
app_publisher = "Jay Kumar Gangani"
app_description = "SFPL Strip Customization"
app_email = "jay@sfpl.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# fixtures = [
#     "Workflow",
#     "Workflow State",
#     "Workflow Action Master"
# ]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sfpl_strip",
# 		"logo": "/assets/sfpl_strip/logo.png",
# 		"title": "SFPL Strip",
# 		"route": "/sfpl_strip",
# 		"has_permission": "sfpl_strip.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sfpl_strip/css/sfpl_strip.css"
# app_include_js = "/assets/sfpl_strip/js/sfpl_strip.js"

# include js, css files in header of web template
# web_include_css = "/assets/sfpl_strip/css/sfpl_strip.css"
# web_include_js = "/assets/sfpl_strip/js/sfpl_strip.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sfpl_strip/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sfpl_strip/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sfpl_strip.utils.jinja_methods",
# 	"filters": "sfpl_strip.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sfpl_strip.install.before_install"
after_install = "sfpl_strip.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sfpl_strip.uninstall.before_uninstall"
# after_uninstall = "sfpl_strip.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sfpl_strip.utils.before_app_install"
# after_app_install = "sfpl_strip.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sfpl_strip.utils.before_app_uninstall"
# after_app_uninstall = "sfpl_strip.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "sfpl_strip.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sfpl_strip.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Strip Work Schedule": "sfpl_strip.custom_query.get_strip_work_schedule",
	"Item": "sfpl_strip.custom_query.get_strip_item"
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sfpl_strip.tasks.all"
# 	],
# 	"daily": [
# 		"sfpl_strip.tasks.daily"
# 	],
# 	"hourly": [
# 		"sfpl_strip.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sfpl_strip.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sfpl_strip.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sfpl_strip.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "sfpl_strip.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sfpl_strip.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sfpl_strip.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sfpl_strip.utils.before_request"]
# after_request = ["sfpl_strip.utils.after_request"]

# Job Events
# ----------
# before_job = ["sfpl_strip.utils.before_job"]
# after_job = ["sfpl_strip.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sfpl_strip.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

