from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'teacher'

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            raise PermissionDenied("You are not allowed to access this page.")
        return super().dispatch(request, *args, **kwargs)