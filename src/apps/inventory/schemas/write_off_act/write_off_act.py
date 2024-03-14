from typing import List, Dict, Optional
from datetime import datetime
from ninja import Schema
from src.apps.inventory.models import WriteOffAct
from src.apps.dictionary.schemas import RegionSchema, DistrictSchema
from src.apps.inventory.services.crud import inventory_unit_crud
from asgiref.sync import sync_to_async


class WriteOffActSchema(Schema):
    id: int
    name_uz: str
    name_ru: Optional[str] = None
    status: str
    inventory_numbers: List[Dict]
    file: str
    region: RegionSchema
    district: DistrictSchema
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def resolve_inventory_numbers(obj):
        inventory_units = obj.inventory_unit_for_write_off_act.all()
        result = []
        for inventory in inventory_units:
            data = dict()
            data["id"] = inventory.id
            data["inventory_number"] = inventory.inventory_number
            result.append(data)
        return result

    @staticmethod
    def resolve_file(obj):
        return obj.file.url
