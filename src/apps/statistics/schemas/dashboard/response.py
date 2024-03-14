from src.apps.statistics.schemas.dashboard.cec_schema import CECUserOut
from src.apps.statistics.schemas.dashboard.region_schema import RegionUserOut
from src.apps.statistics.schemas.dashboard.district_schema import DistrictUserOut
from ninja import Schema
from typing import Optional


class UserOut(Schema):
    cec_user: Optional[CECUserOut] = None
    region_user: Optional[RegionUserOut] = None
    district_user: Optional[DistrictUserOut] = None
