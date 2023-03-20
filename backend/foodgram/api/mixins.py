from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Класс ViewSet только для создания и получения объектов(-а)."""
    pass
