from django.core.exceptions import PermissionDenied


class BuyerRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'buyer':
            raise PermissionDenied("")
        else:
            return super().dispatch(request, *args, **kwargs)
