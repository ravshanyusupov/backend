from src.apps.users.permissions import UserPermission
from src.apps.inventory.schemas import IdProductSchema, ProductDetailSchema
from src.apps.inventory.services.crud import product_crud

permissions = [UserPermission]
response = ProductDetailSchema


async def handler(request, payload: IdProductSchema):
    """
    # Description

    **This endpoint gets a single Product with the provided ID.**

    **Roles:**
    - `CEC User`
    
    - `Region User`

    - `District User`

    """
    instance = await product_crud.read(payload.id, select_related=["category"])

    return instance
