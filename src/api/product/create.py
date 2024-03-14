from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import ProductCreateSchema, ProductDetailSchema
from src.apps.inventory.services.crud import product_crud


permissions = [IsCECUser]
response = {201: ProductDetailSchema}


async def handler(request, payload: ProductCreateSchema):
    """
    # Description

    **This endpoint creates a new Product with the provided payload.**

    **Roles:**
    - `CEC User`
    """
    instance = await product_crud.create(payload.dict(exclude_unset=True))
    instance = await product_crud.read(instance.id, select_related=["category"])

    return instance
