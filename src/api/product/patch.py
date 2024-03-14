from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import ProductPatchSchema, ProductDetailSchema
from src.apps.inventory.services.crud import product_crud

permissions = [IsCECUser]
response = ProductDetailSchema


async def handler(request, payload: ProductPatchSchema):
    """
    # Description

    **This endpoint updates a Product with the provided ID and payload.**

    **Roles:**
    - `CEC User`
    """
    instance = await product_crud.read(payload.id)
    instance = await product_crud.update(instance, payload.dict(exclude_unset=True))
    instance = await product_crud.read(instance.id, ["category"])

    return instance
