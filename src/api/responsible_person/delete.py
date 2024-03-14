from src.apps.dictionary.services.crud import responsible_person_crud
from src.apps.users.services.crud import user_crud
from src.apps.dictionary.schemas import IdResponsiblePersonSchema
from src.apps.dictionary.services.validator import check_district_of_instance
from src.apps.users.permissions import IsDistrictUser

permissions = [IsDistrictUser]
response = {204: None}


async def handler(request, payload: IdResponsiblePersonSchema):
    """
    # Description

    **This endpoint deletes a Responsible Person based on the provided ID.**

    **Roles:**
    - `District User`: <big>**Can delete a Responsible Person if the Responsible Person is in the same district as the user.**</big>

    """
    responsible_person_instance = await responsible_person_crud.read(payload.id)
    await check_district_of_instance(responsible_person_instance, request.user)
    await responsible_person_crud.delete(responsible_person_instance)
    return 204, None
