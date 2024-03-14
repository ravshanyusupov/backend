from src.apps.dictionary.services.crud import responsible_person_crud
from src.apps.users.services.crud import user_crud
from src.apps.dictionary.schemas import (
    CreateResponsiblePersonSchema,
    ResponsiblePersonSchema,
)
from src.apps.users.permissions import IsDistrictUser

permissions = [IsDistrictUser]
response = {201: ResponsiblePersonSchema}


async def handler(request, payload: CreateResponsiblePersonSchema):
    """
    # Description

    **This endpoint creates a new Responsible Person with the provided payload.**

    **Roles:**
    - `District User`
    """
    user = request.user
    data = payload.dict()
    data.update(
        {
            "region_id": user.region_id,
            "district_id": user.district_id,
        }
    )
    instance = await responsible_person_crud.create(data)
    instance = await responsible_person_crud.read(
        instance.id, select_related=["region", "district"]
    )
    return 201, instance
