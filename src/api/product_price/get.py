from src.apps.users.permissions import UserPermission
from src.apps.inventory.schemas import IdProductPriceSchema, ProductPriceDetailSchema
from src.apps.inventory.services.crud import product_price_crud

permissions = [UserPermission]
response = ProductPriceDetailSchema


async def handler(request, payload: IdProductPriceSchema):
    """
    # Description

    **This endpoint gets a single Product Price with the provided ID.**

    **Roles:**
    - `CEC User`

    - `Region User`

    - `District User`

    """
    instance = await product_price_crud.read(
        payload.id, select_related=["product__category", "year"]
    )

    return instance
