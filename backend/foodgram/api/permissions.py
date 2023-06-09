from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsReadOnly(BasePermission):
    """Перминш для изменение моделей только авторам или админу."""
    def has_permission(self, request, view):
        """GET-запрос не требует авторизации."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Пользователь User не может редактировать чужой пост."""
        return (
            request.method in SAFE_METHODS or obj.author == request.user
            or request.user.is_admin
        )
