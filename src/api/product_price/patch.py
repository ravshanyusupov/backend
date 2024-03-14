from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import ProductPricePatchSchema, ProductPriceDetailSchema
from src.apps.inventory.services.crud import product_price_crud

permissions = [IsCECUser]
response = ProductPriceDetailSchema


async def handler(request, payload: ProductPricePatchSchema):
    """
    # Description

    **This endpoint updates a Product Price with the provided ID and payload.**

    **Roles:**
    - `CEC User`

    """
    instance = await product_price_crud.read(payload.id)
    instance = await product_price_crud.update(
        instance, payload.dict(exclude_unset=True)
    )
    instance = await product_price_crud.read(instance.id, ["product__category", "year"])

    return instance
