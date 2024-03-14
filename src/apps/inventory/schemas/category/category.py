from ninja import ModelSchema
from src.apps.inventory.models import Category


class CategoryDetailSchema(ModelSchema):
    class Meta:
        model = Category
        fields = "__all__"
