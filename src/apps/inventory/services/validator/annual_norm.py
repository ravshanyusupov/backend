from ninja_lib.error import DomainException
from src.apps.users.models import User


class AnnualNormDomain:
    def __init__(self, user, data) -> None:
        self.user = user
        self.user_type = user.user_type
        self.data = data


class AnnualNormCore(AnnualNormDomain):
    async def check_instance_for_district(self):
        if self.data.district and self.user_type == User.CEC:
            raise DomainException(4011)
        if not self.data.district and self.user_type == User.REGION:
            raise DomainException(4011)

    async def check_instance_region_id(self):
        if not (self.data.region_id == self.user.region_id):
            raise DomainException(4011)


class AnnualNorm(AnnualNormCore):
    async def validator(self):
        filters = {
            User.CEC: self.check_cec_user,
            User.REGION: self.check_region_user,
        }

        await filters.get(self.user_type)()

    async def check_cec_user(self):
        await self.check_instance_for_district()

    async def check_region_user(self):
        await self.check_instance_for_district()
        await self.check_instance_region_id()
