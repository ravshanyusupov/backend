from src.apps.dictionary.schemas import (
    ResponsiblePersonPatchSchema,
    ResponsiblePersonSchema,
)
from src.apps.dictionary.services.crud import responsible_person_crud
from src.apps.dictionary.services.validator import check_district_of_instance
from src.apps.users.services.crud import user_crud
from src.apps.users.permissions import IsDistrictUser


permissions = [IsDistrictUser]
response = {200: ResponsiblePersonSchema}


async def handler(request, payload: ResponsiblePersonPatchSchema):
    """
    # Description

    **This endpoint updates a Responsible Person based on the provided ID and payload.**

    **Roles:**
    - `District User`: <big>**Can update a Responsible Person if the Responsible Person is in the same district as the user.**</big>

    """
    instance_id = payload.id
    responsible_person_instance = await responsible_person_crud.read(instance_id)
    await check_district_of_instance(responsible_person_instance, request.user)
    updated_instance = await responsible_person_crud.update(
        responsible_person_instance, payload.dict(exclude_unset=True)
    )
    updated_instance = await responsible_person_crud.read(
        responsible_person_instance.id, select_related=["region", "district"]
    )
    return 200, updated_instance
