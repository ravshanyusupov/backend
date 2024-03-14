from tests.fixtures import *

from tests.factories.users import CecUserFactory, RegionUserFactory, DistrictUserFactory
from tests.factories.dictionary import (
    RegionFactory,
    DistrictFactory,
    BuildingCategoryFactory,
    StoragePlaceFactory,
    ResponsiblePersonFactory,
    YearFactory,
)
from tests.factories.inventory import (
    AnnualNormFactory,
    CategoryFactory,
    InventoryUnitFactory,
    ProductNormFactory,
    ProductPriceFactory,
    ProductFactory,
    WriteOffActFactory,
)

from pytest_factoryboy import register

# DICTIONARY
register(BuildingCategoryFactory)
register(StoragePlaceFactory)
register(DistrictFactory)
register(RegionFactory)
register(ResponsiblePersonFactory)
register(YearFactory)

# USERS
register(CecUserFactory)
register(RegionUserFactory)
register(DistrictUserFactory)

# INVENTORY
register(AnnualNormFactory)
register(CategoryFactory)
register(InventoryUnitFactory)
register(ProductNormFactory)
register(ProductPriceFactory)
register(ProductFactory)
register(WriteOffActFactory)
