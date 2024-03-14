from asgiref.sync import sync_to_async
from django.db.models import Q


class CRUD_Queryset:
    def __init__(self, Model):
        self.Model = Model

    async def read(self, pk: int, select_related: list = [], prefetch_related: list = []):
        return await (self.Model.objects.select_related(*select_related).prefetch_related(*prefetch_related).aget(pk=pk))

    async def get_list(
        self,
        ordering: list = ["-created_at", "-updated_at"],
        select_related: list = [],
        prefetch_related: list = [],
        conditions: Q = Q(),
    ):
        return await sync_to_async(list)(
            self.Model.objects.select_related(*select_related)
            .prefetch_related(*prefetch_related)
            .filter(conditions)
            .order_by(*ordering)
        )

    async def get_queryset(
        self,
        select_related: list = [],
        prefetch_related: list = [],
        conditions: Q = Q(),
    ):
        return await sync_to_async(
            self.Model.objects.select_related(*select_related)
            .prefetch_related(*prefetch_related)
            .filter
        )(conditions)

    async def create(self, data_dict: dict = {  }):
        return await self.Model.objects.acreate(**data_dict)

    async def update(self, instance, data_dict: dict = {}):
        for attr, value in data_dict.items():
            setattr(instance, attr, value)
        await instance.asave()
        return instance

    async def delete(self, instance):
        return await instance.adelete()
