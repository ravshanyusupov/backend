from ninja import ModelSchema
from src.apps.inventory.models import ProductPrice
from src.apps.inventory.schemas import ProductDetailSchema
from src.apps.dictionary.schemas import YearDetailSchema


class ProductPriceDetailSchema(ModelSchema):
    product: ProductDetailSchema
    year: YearDetailSchema

    class Meta:
        model = ProductPrice
        fields = "__all__"
