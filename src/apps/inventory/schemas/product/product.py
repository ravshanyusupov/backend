from ninja import ModelSchema
from src.apps.inventory.schemas import CategoryDetailSchema
from src.apps.inventory.models import Product


class ProductDetailSchema(ModelSchema):
    category: CategoryDetailSchema

    class Meta:
        model = Product
        fields = "__all__"
