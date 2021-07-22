from django.utils.translation import gettext as _


class Messages:
    DATABASE_ERROR = [
        {
            "message": _("Internal server error."),
            "code": "internal_server_error"
        }
    ]
    PERMISSION_DENIED_ERROR = [
        {
            "message": _("You don't have the permission to access this resource."),
            "code": "permission_denied"
        }
    ]
