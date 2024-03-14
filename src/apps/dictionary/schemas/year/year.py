from ninja import ModelSchema
from src.apps.dictionary.models import Year


class YearDetailSchema(ModelSchema):
    class Meta:
        model = Year
        fields = ["id", "year"]
